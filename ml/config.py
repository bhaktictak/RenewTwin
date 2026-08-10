try:
    import torch
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
except ImportError:
    DEVICE = 'cpu'

NUM_CLASSES = 4
DEFECT_CLASSES = ['none', 'crack', 'hotspot', 'inactive']
IMAGE_SIZE = 224
BATCH_SIZE = 32
LR = 0.001
NUM_EPOCHS = 20
MODEL_SAVE_PATH = 'ml/models/defect_classifier.pth'
