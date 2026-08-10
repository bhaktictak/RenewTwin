import os
import argparse
import torch
import numpy as np
from PIL import Image
from torchvision import transforms
from ml.config import NUM_CLASSES, DEFECT_CLASSES, MODEL_SAVE_PATH, DEVICE, IMAGE_SIZE
from ml.model import get_model

def load_model(model_path):
    model = get_model(NUM_CLASSES).to(DEVICE)
    if os.path.exists(model_path):
        model.load_state_dict(torch.load(model_path, map_location=DEVICE))
        model.eval()
        return model
    return None

def predict_image(model, image_path):
    if model is None:
        # DEMO INFERENCE using image stats
        print("DEMO_INFERENCE: No model found, using heuristics.")
        try:
            img = Image.open(image_path).convert('L')
            arr = np.array(img)
            mean_val = np.mean(arr)
            std_val = np.std(arr)
            
            # Simple heuristic
            if std_val > 50:
                cls_idx = 1 # crack
            elif mean_val > 150:
                cls_idx = 2 # hotspot
            elif mean_val < 50:
                cls_idx = 3 # inactive
            else:
                cls_idx = 0 # none
                
            probs = [0.1, 0.1, 0.1, 0.1]
            probs[cls_idx] = 0.7
            return {
                'defect_class': DEFECT_CLASSES[cls_idx],
                'probabilities': probs,
                'confidence': 0.7,
                'is_demo': True
            }
        except Exception as e:
            print(f"Error processing image: {e}")
            return None

    # Real inference
    transform = transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    image = Image.open(image_path).convert('RGB')
    input_tensor = transform(image).unsqueeze(0).to(DEVICE)
    
    with torch.no_grad():
        output = model(input_tensor)
        probs = torch.nn.functional.softmax(output[0], dim=0)
        conf, cls_idx = torch.max(probs, 0)
        
    return {
        'defect_class': DEFECT_CLASSES[cls_idx.item()],
        'probabilities': probs.cpu().numpy().tolist(),
        'confidence': conf.item(),
        'is_demo': False
    }

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', type=str, required=True, help='Path to image')
    args = parser.parse_args()
    
    model = load_model(MODEL_SAVE_PATH)
    result = predict_image(model, args.image)
    print(result)
