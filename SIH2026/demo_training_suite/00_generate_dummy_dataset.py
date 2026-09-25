"""
SIH 2026: Dummy Dataset Generator for Instant Demo Training
Creates synthetic Indian road images, YOLO label .txt files, and 3D LiDAR point clouds.
"""
import os
import cv2
import numpy as np

def generate_dummy_dataset():
    print("================================================================")
    print("📦 STEP 1: GENERATING SYNTHETIC DUMMY DATASET FOR DEMO TRAINING")
    print("================================================================")

    base_dir = "d:/SIH2026/demo_training_suite/datasets/indian_traffic_dummy"
    train_img_dir = os.path.join(base_dir, "images", "train")
    val_img_dir = os.path.join(base_dir, "images", "val")
    train_lbl_dir = os.path.join(base_dir, "labels", "train")
    val_lbl_dir = os.path.join(base_dir, "labels", "val")
    lidar_dir = os.path.join(base_dir, "lidar_points")

    for d in [train_img_dir, val_img_dir, train_lbl_dir, val_lbl_dir, lidar_dir]:
        os.makedirs(d, exist_ok=True)

    # Class ID mapping:
    # 0: auto_rickshaw, 1: cow_cattle, 2: pedestrian, 3: two_wheeler, 4: pothole, 5: truck_bus, 6: car
    splits = [('train', 40, train_img_dir, train_lbl_dir), ('val', 10, val_img_dir, val_lbl_dir)]

    img_w, img_h = 640, 640

    for split_name, count, img_out, lbl_out in splits:
        print(f"Creating {count} synthetic {split_name} images and YOLO labels...")
        for i in range(count):
            # 1. Base Road Canvas (Dark Asphalt with dirt shoulders)
            img = np.zeros((img_h, img_w, 3), dtype=np.uint8)
            img[:] = (60, 60, 60) # Asphalt color
            
            # Draw roadside dirt edges
            cv2.rectangle(img, (0, 0), (80, img_h), (35, 75, 120), -1) # Brown dirt left
            cv2.rectangle(img, (img_w - 80, 0), (img_w, img_h), (35, 75, 120), -1) # Dirt right

            labels = []

            # 2. Add Synthetic Obstacles & Bounding Boxes
            # Obstacle A: Auto-Rickshaw (Yellow/Green box)
            if np.random.rand() > 0.3:
                ax, ay = np.random.randint(120, 250), np.random.randint(150, 450)
                aw, ah = 70, 90
                cv2.rectangle(img, (ax, ay), (ax + aw, ay + ah), (0, 215, 255), -1)
                cv2.putText(img, "AUTO", (ax, ay - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
                labels.append(f"0 {(ax + aw/2)/img_w:.4f} {(ay + ah/2)/img_h:.4f} {aw/img_w:.4f} {ah/img_h:.4f}")

            # Obstacle B: Cow / Cattle (Brown/White shape)
            if np.random.rand() > 0.4:
                cx, cy = np.random.randint(280, 480), np.random.randint(180, 480)
                cw, ch = 65, 55
                cv2.ellipse(img, (cx + cw//2, cy + ch//2), (cw//2, ch//2), 0, 0, 360, (200, 200, 220), -1)
                cv2.putText(img, "COW", (cx, cy - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
                labels.append(f"1 {(cx + cw/2)/img_w:.4f} {(cy + ch/2)/img_h:.4f} {cw/img_w:.4f} {ch/img_h:.4f}")

            # Obstacle C: Pedestrian
            if np.random.rand() > 0.5:
                px, py = np.random.randint(90, 180), np.random.randint(200, 500)
                pw, ph = 30, 60
                cv2.rectangle(img, (px, py), (px + pw, py + ph), (50, 50, 220), -1)
                labels.append(f"2 {(px + pw/2)/img_w:.4f} {(py + ph/2)/img_h:.4f} {pw/img_w:.4f} {ph/img_h:.4f}")

            # Obstacle D: Pothole (Dark oval on road)
            if np.random.rand() > 0.4:
                pot_x, pot_y = np.random.randint(200, 400), np.random.randint(300, 550)
                pot_w, pot_h = 50, 35
                cv2.ellipse(img, (pot_x + pot_w//2, pot_y + pot_h//2), (pot_w//2, pot_h//2), 0, 0, 360, (25, 25, 25), -1)
                cv2.putText(img, "POTHOLE", (pot_x, pot_y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 200, 255), 1)
                labels.append(f"4 {(pot_x + pot_w/2)/img_w:.4f} {(pot_y + pot_h/2)/img_h:.4f} {pot_w/img_w:.4f} {pot_h/img_h:.4f}")

            # Save Image and YOLO Label file
            img_path = os.path.join(img_out, f"sample_{split_name}_{i:03d}.jpg")
            lbl_path = os.path.join(lbl_out, f"sample_{split_name}_{i:03d}.txt")

            cv2.imwrite(img_path, img)
            with open(lbl_path, 'w') as f:
                f.write("\n".join(labels))

    # 3. Create Sample 3D LiDAR Point Clouds (.bin files)
    print("Creating synthetic 3D LiDAR point clouds...")
    for i in range(10):
        # 1000 random points representing road ground plane + obstacle points
        road_pts = np.random.uniform([-20, 0, -1.8], [20, 60, -1.7], size=(1500, 3))
        obs_pts = np.random.uniform([0, 15, -1.0], [2, 20, 0.5], size=(200, 3))
        intensity = np.random.uniform(0.1, 0.9, size=(1700, 1))
        all_pts = np.hstack([np.vstack([road_pts, obs_pts]), intensity]).astype(np.float32)
        
        bin_path = os.path.join(lidar_dir, f"lidar_frame_{i:03d}.bin")
        all_pts.tofile(bin_path)

    print("✔️ Dummy Dataset generated successfully in:")
    print(f"   {base_dir}")
    print("================================================================\n")

if __name__ == "__main__":
    generate_dummy_dataset()
