# AI/ML Methodology (PROTOTYPE)

## Problem Formulation
The objective is to accurately identify physical defects in solar panels and detect operational anomalies to predict potential failure modes. This is formulated as a dual-task problem:
1. **Multi-class Image Classification**: Categorizing panel images into defect classes.
2. **Unsupervised Anomaly Detection**: Identifying deviations in continuous operational telemetry.

## Data Pipeline
*Note: All current implementation relies on synthetic demo data for pipeline demonstration.*

1. **Visual Data**: Target dataset is the ELPV Electroluminescence dataset. Images will be resized to 224x224, normalized using ImageNet statistics, and augmented (rotations, flips) during training.
2. **Telemetry Data**: Simulated variables including current, voltage, and temperature, generated with added Gaussian noise to mimic operational environments.

## Model Selection Rationale

### Visual Defect Detection: ResNet-18
- **Why**: ResNet-18 offers a proven, robust architecture for image classification. It is lightweight enough to allow rapid fine-tuning and provides an excellent accuracy-to-latency ratio suitable for prototype development and future edge deployment.
- **Pre-training**: Weights pre-trained on ImageNet.

### Operational Anomaly Detection: Isolation Forest
- **Why**: Isolation Forest is highly effective for tabular anomaly detection, requiring minimal hyperparameter tuning and performing well without labeled anomaly data.

## Training Procedure (Target)
- **Optimizer**: Adam
- **Loss Function**: Cross-Entropy Loss for multi-class classification.
- **Learning Rate**: 1e-4 with step learning rate scheduling.
- **Hardware**: Training leveraging NVIDIA CUDA GPUs.

## Evaluation Metrics
- **Visual Model**: Accuracy, Precision, Recall, and F1-Score per class.
- **Anomaly Model**: Evaluated heuristically based on synthetic boundary detection.

## Digital Twin Health Scoring
The prototype Asset Health Index aggregates model outputs. The formula applies weighted penalties for recognized visual defects and high anomaly scores, representing the composite degradation of the asset.

*All claims and results presented in the prototype phase are for demonstration of the digital asset management pipeline.*
