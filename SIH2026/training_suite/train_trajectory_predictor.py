"""
SIH 2026: Multi-Agent Trajectory Prediction Neural Network (PyTorch)
Predicts non-linear future motion (next 1-3s) for cattle, pedestrians, and bikes.
"""
import torch
import torch.nn as nn
import numpy as np

class TrajectoryPredictorGRU(nn.Module):
    """Sequence-to-Sequence GRU for Multi-Agent Motion Forecasting."""
    def __init__(self, input_dim=2, hidden_dim=64, output_dim=2, pred_len=12): # 12 steps = 2.4s (dt=0.2)
        super().__init__()
        self.pred_len = pred_len
        self.encoder = nn.GRU(input_dim, hidden_dim, batch_first=True)
        self.decoder_cell = nn.GRUCell(output_dim, hidden_dim)
        self.fc_out = nn.Linear(hidden_dim, output_dim)

    def forward(self, past_trajectories):
        # past_trajectories: [batch_size, seq_len, 2] (past 8 steps = 1.6s)
        _, hidden = self.encoder(past_trajectories)
        hidden = hidden.squeeze(0) # [batch_size, hidden_dim]

        batch_size = past_trajectories.size(0)
        decoder_input = past_trajectories[:, -1, :] # Start from last known position

        outputs = []
        for _ in range(self.pred_len):
            hidden = self.decoder_cell(decoder_input, hidden)
            pred_step = self.fc_out(hidden)
            outputs.append(pred_step.unsqueeze(1))
            decoder_input = pred_step

        return torch.cat(outputs, dim=1) # [batch_size, pred_len, 2]

def train_trajectory_model():
    print("================================================================")
    print("🚀 SIH 2026: TRAINING TRAJECTORY PREDICTION MODEL (GRU)")
    print("================================================================")

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Device: {device}")

    # Generate synthetic Indian non-lane traffic trajectory sequences for training
    print("\n[Step 1/3] Generating diverse Indian road trajectory training data...")
    num_samples = 3000
    past_len = 8   # 1.6s history
    pred_len = 12  # 2.4s future forecast
    dt = 0.2

    # Synthetic non-lane curves (erratic cattle crossing, turning bikes, straight vehicles)
    X_train = []
    Y_train = []

    for _ in range(num_samples):
        # Random initial velocity and non-linear turn rate
        v = np.random.uniform(1.0, 10.0)
        heading = np.random.uniform(-np.pi, np.pi)
        yaw_rate = np.random.choice([0.0, 0.2, -0.2, 0.4, -0.4]) # Simulates cattle drift or bike turns

        total_len = past_len + pred_len
        traj = []
        cx, cy, ch = 0.0, 0.0, heading

        for _ in range(total_len):
            cx += v * np.cos(ch) * dt + np.random.normal(0, 0.05)
            cy += v * np.sin(ch) * dt + np.random.normal(0, 0.05)
            ch += yaw_rate * dt
            traj.append([cx, cy])

        X_train.append(traj[:past_len])
        Y_train.append(traj[past_len:])

    X_tensor = torch.tensor(np.array(X_train), dtype=torch.float32).to(device)
    Y_tensor = torch.tensor(np.array(Y_train), dtype=torch.float32).to(device)

    # Instantiate Model, Loss and Optimizer
    model = TrajectoryPredictorGRU(pred_len=pred_len).to(device)
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.003)

    print("\n[Step 2/3] Training Neural Network for 40 Epochs...")
    batch_size = 64
    dataset = torch.utils.data.TensorDataset(X_tensor, Y_tensor)
    loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)

    for epoch in range(1, 41):
        total_loss = 0.0
        for bx, by in loader:
            optimizer.zero_grad()
            pred = model(bx)
            loss = criterion(pred, by)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        if epoch % 10 == 0 or epoch == 1:
            avg_loss = total_loss / len(loader)
            print(f"  Epoch [{epoch}/40] - ADE Loss (Average Displacement Error): {avg_loss:.4f} m^2")

    # Save PyTorch Model
    torch.save(model.state_dict(), "d:/SIH2026/training_suite/trajectory_model.pth")
    print("\n✔️ PyTorch Model weights saved: trajectory_model.pth")

    # Export to ONNX for MATLAB
    print("\n[Step 3/3] Exporting to ONNX for MATLAB...")
    dummy_input = torch.randn(1, past_len, 2).to(device)
    onnx_path = "d:/SIH2026/training_suite/trajectory_predictor.onnx"
    torch.onnx.export(
        model,
        dummy_input,
        onnx_path,
        input_names=['past_trajectory'],
        output_names=['future_trajectory'],
        opset_version=12
    )
    print(f"✔️ MATLAB ONNX Model saved at: {onnx_path}")
    print("================================================================\n")

if __name__ == "__main__":
    train_trajectory_model()
