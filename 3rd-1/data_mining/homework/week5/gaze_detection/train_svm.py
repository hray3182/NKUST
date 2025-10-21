import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_curve,
    roc_auc_score,
    classification_report,
)
import joblib
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def load_and_preprocess_data(csv_path, eye_blink_threshold=0.5):
    """
    Load dataset and filter out frames where eyes are closed.

    Args:
        csv_path: Path to the combined CSV file
        eye_blink_threshold: Threshold for eye blink filtering

    Returns:
        X: Feature matrix
        y: Labels
        feature_names: List of feature names
    """
    logging.info(f"Loading data from {csv_path}")
    df = pd.read_csv(csv_path)

    logging.info(f"Initial dataset shape: {df.shape}")
    logging.info(f"Class distribution:\n{df['label'].value_counts()}")

    # Filter out frames where eyes are closed
    before_filter = len(df)
    df = df[(df['eyeBlinkLeft'] < eye_blink_threshold) &
            (df['eyeBlinkRight'] < eye_blink_threshold)]
    after_filter = len(df)
    logging.info(f"Filtered out {before_filter - after_filter} frames with closed eyes")
    logging.info(f"Dataset shape after filtering: {df.shape}")

    # Define features to use
    eye_gaze_features = [
        'eyeLookUpLeft', 'eyeLookUpRight',
        'eyeLookDownLeft', 'eyeLookDownRight',
        'eyeLookInLeft', 'eyeLookInRight',
        'eyeLookOutLeft', 'eyeLookOutRight'
    ]

    head_rotation_features = ['head_pitch', 'head_yaw', 'head_roll']

    feature_names = eye_gaze_features + head_rotation_features

    # Extract features and labels
    X = df[feature_names].values
    y = df['label'].map({'yes': 1, 'no': 0}).values

    logging.info(f"Features used ({len(feature_names)}): {feature_names}")
    logging.info(f"Final dataset shape: X={X.shape}, y={y.shape}")
    logging.info(f"Class distribution - Yes: {np.sum(y == 1)}, No: {np.sum(y == 0)}")

    return X, y, feature_names


def plot_confusion_matrix(cm, output_path):
    """Plot and save confusion matrix."""
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['No', 'Yes'], yticklabels=['No', 'Yes'])
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    logging.info(f"Confusion matrix saved to {output_path}")


def plot_roc_curve(fpr, tpr, auc, output_path):
    """Plot and save ROC curve."""
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {auc:.4f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Classifier')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend(loc="lower right")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    logging.info(f"ROC curve saved to {output_path}")


def train_svm_with_grid_search(X_train, y_train, X_test, y_test, output_dir):
    """
    Train SVM with RBF kernel and hyperparameter tuning.

    Args:
        X_train, y_train: Training data
        X_test, y_test: Testing data
        output_dir: Directory to save results

    Returns:
        best_model: Trained SVM model with best hyperparameters
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Standardize features (important for SVM)
    logging.info("Standardizing features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Define hyperparameter grid for RBF kernel
    param_grid = {
        'C': [0.1, 1, 10, 100, 1000],
        'gamma': [0.001, 0.01, 0.1, 1, 'scale', 'auto']
    }

    logging.info("Starting GridSearchCV for RBF kernel...")
    logging.info(f"Parameter grid: {param_grid}")

    # GridSearchCV with cross-validation
    svm = SVC(kernel='rbf', random_state=42, probability=True)
    grid_search = GridSearchCV(
        svm,
        param_grid,
        cv=5,  # 5-fold cross-validation
        scoring='accuracy',
        n_jobs=-1,
        verbose=2
    )

    grid_search.fit(X_train_scaled, y_train)

    # Get best model
    best_model = grid_search.best_estimator_
    best_params = grid_search.best_params_
    best_cv_score = grid_search.best_score_

    logging.info(f"\n{'='*60}")
    logging.info(f"Best hyperparameters: {best_params}")
    logging.info(f"Best cross-validation accuracy: {best_cv_score:.4f}")
    logging.info(f"{'='*60}\n")

    # Save grid search results
    results_df = pd.DataFrame(grid_search.cv_results_)
    results_df = results_df.sort_values('rank_test_score')
    results_df.to_csv(output_dir / 'grid_search_results.csv', index=False)
    logging.info(f"Grid search results saved to {output_dir / 'grid_search_results.csv'}")

    # Print top 10 parameter combinations
    logging.info("\nTop 10 parameter combinations:")
    top_results = results_df[['params', 'mean_test_score', 'std_test_score', 'rank_test_score']].head(10)
    for idx, row in top_results.iterrows():
        logging.info(f"Rank {int(row['rank_test_score'])}: {row['params']} - "
                    f"Accuracy: {row['mean_test_score']:.4f} (+/- {row['std_test_score']:.4f})")

    # Evaluate on test set
    y_pred = best_model.predict(X_test_scaled)
    y_pred_proba = best_model.predict_proba(X_test_scaled)[:, 1]

    # Calculate all 7 metrics
    logging.info(f"\n{'='*60}")
    logging.info("Test Set Evaluation Metrics:")
    logging.info(f"{'='*60}")

    # 1. Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    logging.info(f"\n1. Confusion Matrix:\n{cm}")
    plot_confusion_matrix(cm, output_dir / 'confusion_matrix.png')

    # 2. Accuracy
    accuracy = accuracy_score(y_test, y_pred)
    logging.info(f"\n2. Accuracy: {accuracy:.4f}")

    # 3. Precision
    precision = precision_score(y_test, y_pred)
    logging.info(f"3. Precision: {precision:.4f}")

    # 4. Recall
    recall = recall_score(y_test, y_pred)
    logging.info(f"4. Recall: {recall:.4f}")

    # 5. F1 Score
    f1 = f1_score(y_test, y_pred)
    logging.info(f"5. F1 Score: {f1:.4f}")

    # 6 & 7. ROC Curve and AUC
    fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
    auc = roc_auc_score(y_test, y_pred_proba)
    logging.info(f"6. ROC Curve: Saved to file")
    logging.info(f"7. AUC: {auc:.4f}")
    plot_roc_curve(fpr, tpr, auc, output_dir / 'roc_curve.png')

    # Classification report
    logging.info(f"\nDetailed Classification Report:")
    logging.info(f"\n{classification_report(y_test, y_pred, target_names=['No', 'Yes'])}")

    # Save metrics to file
    metrics = {
        'best_params': best_params,
        'best_cv_accuracy': best_cv_score,
        'test_accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'auc': auc,
        'confusion_matrix': cm.tolist()
    }

    import json
    with open(output_dir / 'metrics.json', 'w') as f:
        json.dump(metrics, f, indent=4)
    logging.info(f"\nMetrics saved to {output_dir / 'metrics.json'}")

    # Save model and scaler
    joblib.dump(best_model, output_dir / 'best_svm_model.pkl')
    joblib.dump(scaler, output_dir / 'scaler.pkl')
    logging.info(f"Model saved to {output_dir / 'best_svm_model.pkl'}")
    logging.info(f"Scaler saved to {output_dir / 'scaler.pkl'}")

    # Save detailed report to text file
    report_path = output_dir / 'training_report.txt'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write("SVM TRAINING ANALYSIS REPORT\n")
        f.write("="*60 + "\n\n")

        f.write("HYPERPARAMETER TUNING RESULTS\n")
        f.write("-"*60 + "\n")
        f.write(f"Best hyperparameters: {best_params}\n")
        f.write(f"Best cross-validation accuracy: {best_cv_score:.4f}\n\n")

        f.write("Top 10 Parameter Combinations:\n")
        top_results = results_df[['params', 'mean_test_score', 'std_test_score', 'rank_test_score']].head(10)
        for idx, row in top_results.iterrows():
            f.write(f"  Rank {int(row['rank_test_score'])}: {row['params']}\n")
            f.write(f"    Accuracy: {row['mean_test_score']:.4f} (+/- {row['std_test_score']:.4f})\n")
        f.write("\n")

        f.write("="*60 + "\n")
        f.write("TEST SET EVALUATION METRICS\n")
        f.write("="*60 + "\n\n")

        f.write("1. Confusion Matrix:\n")
        f.write(f"   Predicted No  Predicted Yes\n")
        f.write(f"Actual No    {cm[0,0]:5d}      {cm[0,1]:5d}\n")
        f.write(f"Actual Yes   {cm[1,0]:5d}      {cm[1,1]:5d}\n\n")

        f.write(f"2. Accuracy:  {accuracy:.4f}\n")
        f.write(f"3. Precision: {precision:.4f}\n")
        f.write(f"4. Recall:    {recall:.4f}\n")
        f.write(f"5. F1 Score:  {f1:.4f}\n")
        f.write(f"6. ROC Curve: Saved to 'roc_curve.png'\n")
        f.write(f"7. AUC:       {auc:.4f}\n\n")

        f.write("="*60 + "\n")
        f.write("DETAILED CLASSIFICATION REPORT\n")
        f.write("="*60 + "\n")
        f.write(classification_report(y_test, y_pred, target_names=['No', 'Yes']))
        f.write("\n")

        f.write("="*60 + "\n")
        f.write("SUMMARY\n")
        f.write("="*60 + "\n")
        f.write(f"Training samples: {len(X_train)}\n")
        f.write(f"Testing samples:  {len(X_test)}\n")
        f.write(f"Total features:   {X_train.shape[1]}\n")
        f.write(f"Kernel type:      RBF\n")
        f.write(f"Best C parameter: {best_params['C']}\n")
        f.write(f"Best gamma:       {best_params['gamma']}\n")
        f.write("="*60 + "\n")

    logging.info(f"Training report saved to {report_path}")

    logging.info(f"\n{'='*60}")

    return best_model, scaler


def main():
    """Main training pipeline."""
    # Configuration
    csv_path = 'output_features/all_videos_combined.csv'
    output_dir = 'svm_results'
    eye_blink_threshold = 0.5
    test_size = 0.2
    random_state = 42

    # Load and preprocess data
    X, y, feature_names = load_and_preprocess_data(csv_path, eye_blink_threshold)

    # Split data
    logging.info(f"\nSplitting data: {int((1-test_size)*100)}% train, {int(test_size*100)}% test")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    logging.info(f"Training set: {X_train.shape}, Testing set: {X_test.shape}")
    logging.info(f"Train class distribution - Yes: {np.sum(y_train == 1)}, No: {np.sum(y_train == 0)}")
    logging.info(f"Test class distribution - Yes: {np.sum(y_test == 1)}, No: {np.sum(y_test == 0)}")

    # Train model
    best_model, scaler = train_svm_with_grid_search(X_train, y_train, X_test, y_test, output_dir)

    logging.info("\n" + "="*60)
    logging.info("Training completed successfully!")
    logging.info("="*60)


if __name__ == "__main__":
    main()
