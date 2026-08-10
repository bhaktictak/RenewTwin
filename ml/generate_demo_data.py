import os
import numpy as np
from PIL import Image
from ml.config import DEFECT_CLASSES

def generate_synthetic_images(base_dir='ml/data/sample'):
    """Generates synthetic grayscale images for demo purposes."""
    np.random.seed(42)
    os.makedirs(base_dir, exist_ok=True)
    
    for cls_name in DEFECT_CLASSES:
        cls_dir = os.path.join(base_dir, cls_name)
        os.makedirs(cls_dir, exist_ok=True)
        
        for i in range(10):
            # Base smooth gradient
            x = np.linspace(50, 200, 224)
            y = np.linspace(50, 200, 224)
            X, Y = np.meshgrid(x, y)
            img_arr = (X + Y) / 2
            
            if cls_name == 'crack':
                # Add random lines
                for _ in range(5):
                    x0, y0 = np.random.randint(0, 224, 2)
                    length = np.random.randint(20, 80)
                    angle = np.random.uniform(0, 2*np.pi)
                    for l in range(length):
                        xi = int(x0 + l * np.cos(angle))
                        yi = int(y0 + l * np.sin(angle))
                        if 0 <= xi < 224 and 0 <= yi < 224:
                            img_arr[yi, xi] = 0
            elif cls_name == 'hotspot':
                # Add bright circles
                cx, cy = np.random.randint(20, 200, 2)
                r = np.random.randint(10, 30)
                Y_idx, X_idx = np.ogrid[:224, :224]
                mask = (X_idx - cx)**2 + (Y_idx - cy)**2 <= r**2
                img_arr[mask] = 255
            elif cls_name == 'inactive':
                # Dark rectangles
                x0, y0 = np.random.randint(0, 150, 2)
                w, h = np.random.randint(30, 70, 2)
                img_arr[y0:y0+h, x0:x0+w] = 20
                
            img_arr = np.clip(img_arr, 0, 255).astype(np.uint8)
            img = Image.fromarray(img_arr)
            
            filename = os.path.join(cls_dir, f'synth_{cls_name}_{i:03d}.jpg')
            img.save(filename)
            
    print("SYNTHETIC: Generated 40 images (10 per class)")

def generate_operational_data(filepath='ml/data/sample/operational_data.csv'):
    """Generates synthetic operational data."""
    import csv
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['asset_id', 'timestamp', 'power_kw', 'expected_power_kw', 'temperature_c', 'irradiance'])
        
        for i in range(24):
            asset_id = f'PANEL_{i%4}'
            ts = f'2026-08-10T{i:02d}:00:00Z'
            expected = np.random.uniform(200, 300)
            actual = expected * np.random.uniform(0.7, 1.0)
            temp = np.random.uniform(20, 55)
            irr = np.random.uniform(500, 1000)
            
            writer.writerow([asset_id, ts, round(actual, 2), round(expected, 2), round(temp, 1), round(irr, 1)])
            
    print("SYNTHETIC: Generated 24 rows of operational data")

def generate_all_data():
    generate_synthetic_images()
    generate_operational_data()

if __name__ == '__main__':
    generate_all_data()
