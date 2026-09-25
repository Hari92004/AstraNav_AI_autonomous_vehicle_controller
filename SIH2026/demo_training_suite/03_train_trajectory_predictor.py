"""
SIH 2026: Model 3 - Multi-Agent Trajectory Prediction Neural Network
Predicts 1.0 to 3.0-second future paths for cattle, pedestrians, and weaving two-wheelers.
"""
import torch
import torch.nn as nn
import numpy as np

class TrajectorySeq2SeqGRU(nn.Module):
    """Sequence-to-Sequence Motion Forecast Network."""
    def __init__(self, in_dim=2, hidden_dim=64, out_dim=2, pred_steps=12):
        super().__init__()
        self.pred_steps = pred_steps
        self.encoder = nn.GRU(in_dim, hidden_dim, batch_first=True)
        self.decoder_cell = nn.GRUCell(out_dim, hidden_dim)
        self.fc = nn.Linear(hidden_dim, out_dim)

    def forward(self, history_traj):
        # history_traj: [batch, 8, 2] (past 1.6s)
        _, h = self.encoder(history_traj)
        h = h.squeeze(0)
        curr_pos = history_traj[:, -1, :]
        
        preds = []
        for _ in range(self.pred_steps):
            h = self.decoder_cell(curr_pos, h)
            next_step = self.fc(h)
            preds.append(next_step.unsqueeze(1))
            curr_pos = next_step
            
        return torch.cat(preds, dim=1) # [batch, 12, 2] (next 2.4s)

def run_trajectory_demo_training():
    print("================================================================")
    print("🔮 MODEL 3: TRAINING MULTI-AGENT TRAJECTORY PREDICTION (GRU)")
    print("================================================================")

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Device: {device}")

    # Generate synthetic Indian non-lane traffic trajectory sequences
    num_samples = 300
    past_len = 8   # 1.6s history
    pred_len = 12  # 2.4s future forecast
    dt = 0.2

    X_train, Y_train = [], []
    for _ in range(num_samples):
        v = np.random.uniform(1.0, 8.0)
        heading = np.random.uniform(-np.pi, np.pi)
        yaw_rate = np.random.choice([0.0, 0.25, -0.25])
        traj = []
        x, y = 0.0, 0.0
        for _ in range(past_len + pred_len):
            x += v * np.cos(heading) * dt
            y += v * np.sin(heading) * dt
            heading += yaw_rate * dt
            traj.append([x, y])
        X_train.append(traj[:past_len])
        Y_train.append(traj[past_len:])

    X_tensor = torch.tensor(X_train, dtype=torch.float32).to(device)
    Y_tensor = torch.tensor(Y_train, dtype=torch.float32).to(device)

    model = TrajectorySeq2SeqGRU(pred_steps=pred_len).to(device)
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.003)

    print("Training Trajectory Predictor (15 epochs demo)...")
    dataset = torch.utils.data.TensorDataset(X_tensor, Y_tensor)
    loader = torch.utils.data.DataLoader(dataset, batch_size=32, shuffle=True)

    for epoch in range(1, 16):
        total_loss = 0.0
        for bx, by in loader:
            optimizer.zero_grad()
            pred = model(bx)
            loss = criterion(pred, by)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        if epoch % 5 == 0 or epoch == 1:
            print(f"  Epoch [{epoch:02d}/15] - Displacement Loss (ADE): {total_loss/len(loader):.4f} m^2")

    # Export to ONNX for MATLAB
    print("\nExporting Model 3 to ONNX for MATLAB...")
    dummy_input = torch.randn(1, past_len, 2).to(device)
    onnx_out = "d:/SIH2026/demo_training_suite/trajectory_predictor.onnx"
    torch.onnx.export(model, dummy_input, onnx_out, opset_version=12,
                      input_names=['past_trajectory'], output_names=['future_trajectory'])
    print(f"✔️ Model 3 ONNX Exported: {onnx_out}")
    print("================================================================\n")

if __name__ == "__main__":
    run_trajectory_demo_training()
