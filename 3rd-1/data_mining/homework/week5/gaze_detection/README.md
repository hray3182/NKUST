# Gaze Detection using MediaPipe and SVM

A machine learning project to detect whether a user is watching the screen using facial features from MediaPipe and Support Vector Machine (SVM) classifier.

## Features

- Extract eye gaze and head rotation features from videos using MediaPipe
- Train SVM classifier with RBF kernel
- Real-time gaze detection using webcam
- Achieve 97.7% accuracy on test set

## Requirements

- Python >= 3.8
- uv (Python package manager)

## Installation

### 1. Install uv (if you haven't)

```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or using pip
pip install uv
```

### 2. Clone the repository and setup environment

```bash
cd gaze_detection

# Install dependencies (this will create a virtual environment and install all packages)
uv sync
```

This will install all required packages:
- mediapipe - Face detection and feature extraction
- opencv-python - Video processing
- numpy - Numerical computing
- pandas - Data processing
- scikit-learn - Machine learning (SVM)
- matplotlib, seaborn - Visualization
- joblib - Model persistence

### 3. Download MediaPipe model

Download the face landmarker model from MediaPipe:

```bash
# Download face_landmarker.task
wget https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task
```

Or download manually from: https://developers.google.com/mediapipe/solutions/vision/face_landmarker#models

## Usage

### 1. Extract Features from Videos

First, prepare your dataset with this structure:

```
dataset/
├── yes/        # Videos where you're watching the screen
│   └── *.mp4
└── no/         # Videos where you're not watching the screen
    └── *.mp4
```

Then run the feature extraction script:

```bash
uv run python extract_features.py
```

This will:
- Process every 5th frame of each video
- Extract 8 eye gaze features and 3 head rotation features
- Filter out frames where eyes are closed
- Save features to CSV files in `output_features/`
- Create a combined CSV file: `output_features/all_videos_combined.csv`

### 2. Train SVM Classifier

After extracting features, train the SVM model:

```bash
uv run python train_svm.py
```

This will:
- Load features from `output_features/all_videos_combined.csv`
- Split data into 80% training and 20% testing
- Perform hyperparameter tuning using GridSearchCV
- Train SVM with RBF kernel
- Evaluate model with 7 metrics:
  - Confusion Matrix
  - Accuracy
  - Precision
  - Recall
  - F1 Score
  - ROC Curve
  - AUC
- Save results to `svm_results/`:
  - `best_svm_model.pkl` - Trained model
  - `scaler.pkl` - Feature scaler
  - `confusion_matrix.png` - Confusion matrix visualization
  - `roc_curve.png` - ROC curve visualization
  - `metrics.json` - All evaluation metrics
  - `grid_search_results.csv` - Hyperparameter tuning results

### 3. Real-time Prediction

Test the trained model with your webcam:

```bash
uv run python realtime_prediction.py
```

This will:
- Open your webcam
- Detect your face in real-time
- Extract features and predict whether you're watching the screen
- Display results with color-coded UI:
  - Green: Watching screen
  - Red: Not watching
  - Gray: Eyes closed

Controls:
- `q` - Quit
- `s` - Save screenshot
- `r` - Reset prediction history

## Project Structure

```
gaze_detection/
├── dataset/                    # Video dataset
│   ├── yes/                   # Positive samples
│   └── no/                    # Negative samples
├── output_features/           # Extracted features (CSV)
├── svm_results/              # Training results
│   ├── best_svm_model.pkl
│   ├── scaler.pkl
│   ├── confusion_matrix.png
│   ├── roc_curve.png
│   └── metrics.json
├── extract_features.py       # Script 1: Feature extraction
├── train_svm.py             # Script 2: Model training
├── realtime_prediction.py   # Script 3: Real-time testing
├── mirror_videos.sh         # Data augmentation script
├── face_landmarker.task     # MediaPipe model
├── pyproject.toml           # Project dependencies
├── uv.lock                  # Lock file
└── README.md
```

## Data Augmentation

To improve model generalization, you can apply horizontal mirroring to your videos:

```bash
./mirror_videos.sh
```

This will create mirrored versions of all videos with `_mirrored` suffix.

## Model Performance

After training, the model achieves:
- Accuracy: 97.7%
- Precision: 97.98%
- Recall: 98.18%
- F1 Score: 98.08%
- AUC: 99.64%

## How It Works

1. **Feature Extraction**: MediaPipe detects face landmarks and extracts:
   - 8 eye gaze features (eyeLookUp/Down/In/Out for left/right)
   - 3 head rotation features (pitch, yaw, roll)

2. **Classification**: SVM with RBF kernel learns the non-linear relationship between eye gaze and head pose. The key insight is the "compensation effect" - when the head turns but the user still watches the screen, the eyes compensate by looking in the opposite direction.

3. **Real-time Prediction**: The trained model can predict gaze direction in real-time using webcam input.

## Troubleshooting

### Camera not opening
- Check if your webcam is working: `ls /dev/video*`
- Make sure no other application is using the webcam

### MediaPipe model not found
- Make sure `face_landmarker.task` is in the project root
- Download from the link in Installation section

### Low accuracy
- Make sure you have enough training data (at least 10+ videos per class)
- Check if eyes-closed frames are properly filtered
- Try data augmentation with `mirror_videos.sh`

## License

This project is for educational purposes (Homework 3 - Data Mining Course).

## Acknowledgments

- MediaPipe for face detection and feature extraction
- scikit-learn for SVM implementation
- AI assistance for code development (as documented in chatGPT.md)
