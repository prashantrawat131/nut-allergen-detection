import numpy as np
from preprocess_and_extract import load_all_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib

# Load data
X_pca, X_plsr, y = load_all_data(patch_size=20, n_components=10)

def evaluate_model_with_validation(X, y, name="Feature"):
    print(f"\nEvaluating with {name} features:")

    # Split data into 90% training and 10% validation
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.1, random_state=42, stratify=y
    )

    # Stratified K-Fold on the training set
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    clf = RandomForestClassifier(n_estimators=100, random_state=42)

    all_preds = []
    all_true = []

    for train_idx, test_idx in skf.split(X_train, y_train):
        clf.fit(X_train[train_idx], y_train[train_idx])
        preds = clf.predict(X_train[test_idx])
        all_preds.extend(preds)
        all_true.extend(y_train[test_idx])

    # Classification report and confusion matrix for K-Fold
    print("\n--- K-Fold Evaluation ---")
    print(classification_report(all_true, all_preds))
    print("Confusion Matrix (K-Fold):\n", confusion_matrix(all_true, all_preds))

    # Evaluate on the validation set
    val_preds = clf.predict(X_val)
    print("\n--- Validation Set Evaluation ---")
    print(classification_report(y_val, val_preds))
    print("Confusion Matrix (Validation Set):\n", confusion_matrix(y_val, val_preds))

    return clf

# Evaluate both feature sets with validation
model_pca = evaluate_model_with_validation(X_pca, y, name="PCA")
model_plsr = evaluate_model_with_validation(X_plsr, y, name="PLSR")

# Save models and data for visualization
joblib.dump(model_pca, 'model_pca.pkl')
joblib.dump(model_plsr, 'model_plsr.pkl')
joblib.dump(X_pca, 'X_pca.pkl')
joblib.dump(X_plsr, 'X_plsr.pkl')
joblib.dump(y, 'y.pkl')
joblib.dump(np.unique(y), 'class_names.pkl')