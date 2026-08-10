import torch.nn as nn
from torchvision import models

class SolarDefectClassifier(nn.Module):
    """ResNet18-based classifier for solar panel defects."""
    def __init__(self, num_classes, pretrained=True):
        super().__init__()
        weights = models.ResNet18_Weights.DEFAULT if pretrained else None
        self.model = models.resnet18(weights=weights)
        
        # Freeze early layers
        for name, param in self.model.named_parameters():
            if 'layer1' in name or 'layer2' in name or 'conv1' in name or 'bn1' in name:
                param.requires_grad = False
                
        # Replace fully connected layer
        num_ftrs = self.model.fc.in_features
        self.model.fc = nn.Linear(num_ftrs, num_classes)
        
    def forward(self, x):
        return self.model(x)

def get_model(num_classes, pretrained=True):
    return SolarDefectClassifier(num_classes, pretrained)
