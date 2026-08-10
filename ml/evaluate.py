import os
import json
import argparse
import torch
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
import seaborn as sns
from ml.config import NUM_CLASSES, DEFECT_CLASSES, MODEL_SAVE_PATH, DEVICE, BATCH_SIZE
from ml.dataset import get_dataloaders
from ml.model import get_model
from ml.generate_demo_data import generate_all_data

def evaluate_model(data_dir):
    _, val_loader = get_dataloaders(data_dir, BATCH_SIZE)
    model = get_model(NUM_CLASSES).to(DEVICE)
    
    if os.path.exists(MODEL_SAVE_PATH):
        model.load_state_dict(torch.load(MODEL_SAVE_PATH, map_location=DEVICE))
    else:
        print("Model not found. Evaluating with random weights.")
        
    model.eval()
    all_preds = []
    all_labels = []
    
    with torch.no_grad():
        for inputs, labels in val_loader:
            inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
            
    acc = accuracy_score(all_labels, all_preds)
    precision, recall, f1, _ = precision_recall_fscore_support(all_labels, all_preds, average='macro', zero_division=0)
    per_class_p, per_class_r, per_class_f1, _ = precision_recall_fscore_support(all_labels, all_preds, average=None, zero_division=0)
    
    metrics = {
        'accuracy': acc,
        'precision_macro': precision,
        'recall_macro': recall,
        'f1_macro': f1,
        'per_class': {
            cls_name: {
                'precision': float(per_class_p[i]),
                'recall': float(per_class_r[i]),
                'f1': float(per_class_f1[i])
            } for i, cls_name in enumerate(DEFECT_CLASSES) if i < len(per_class_p)
        }
    }
    
    os.makedirs('ml', exist_ok=True)
    with open('ml/evaluation_metrics.json', 'w') as f:
        json.dump(metrics, f, indent=4)
        
    # Confusion matrix plot
    cm = confusion_matrix(all_labels, all_preds)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=DEFECT_CLASSES, yticklabels=DEFECT_CLASSES)
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix')
    
    os.makedirs('docs/screenshots', exist_ok=True)
    plt.savefig('docs/screenshots/confusion_matrix.png')
    plt.close()
    
    print("Evaluation complete. Metrics saved.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default='ml/data/sample', help='Path to dataset')
    parser.add_argument('--demo', action='store_true', help='Generate synthetic data before evaluate')
    args = parser.parse_args()
    
    if args.demo:
        print("DEMO MODE: Generating synthetic data...")
        generate_all_data()

    evaluate_model(args.data_dir)
