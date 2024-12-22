from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from joblib import dump, load
import numpy as np

X = [
    [10, 1, 1, 3, 12], [30, 0, 2, 0, 25], [15, 1, 3, 2, 18], [40, 0, 3, 0, 32],
    [20, 1, 2, 4, 15], [35, 0, 2, 1, 22], [25, 1, 1, 5, 10], [45, 0, 3, 0, 35],
    [18, 1, 2, 3, 14], [32, 0, 3, 1, 28]
]
y = [1, 1, 2, 2, 1, 2, 1, 2, 1, 2]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

param_grid = {
    "n_estimators": [50, 100, 200],
    "max_depth": [5, 10, None],
    "min_samples_split": [2, 5],
    "min_samples_leaf": [1, 2],
}

grid_search = GridSearchCV(RandomForestClassifier(), param_grid, cv=3, scoring='accuracy')
grid_search.fit(X_scaled, y)
model = grid_search.best_estimator_

dump(model, "optimized_rf_model.joblib")
dump(scaler, "scaler.joblib")

scores = cross_val_score(model, X_scaled, y, cv=3)
print("Cross-validation accuracy:", scores.mean())

feature_names = ["time_taken", "correct", "current_difficulty", "success_streak", "avg_time_last_3"]
importances = model.feature_importances_
print("Feature importances:")
for name, importance in zip(feature_names, importances):
    print(f"{name}: {importance:.4f}")

y_pred = model.predict(X_scaled)
print("\nClassification Report:")
print(classification_report(y, y_pred))

def predict_difficulty(time_taken, correct, current_difficulty, success_streak, avg_time_last_3):
    model = load("optimized_rf_model.joblib")
    scaler = load("scaler.joblib")
    scaled_input = scaler.transform([[time_taken, correct, current_difficulty, success_streak, avg_time_last_3]])
    return model.predict(scaled_input)[0]

print("Predicted Difficulty:", predict_difficulty(12, 1, 2, 4, 15))
