import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score, roc_auc_score, confusion_matrix

df = pd.read_csv("dataset/mouse_activity_filtered.csv")

df.drop(columns=["Timestamp"], inplace=True)
X = df.drop(columns=["Label"])
y = df["Label"]

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.5, random_state=42
)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

models = {
    "Logistic Regression": LogisticRegression(random_state=42),
    "Random Forest": RandomForestClassifier(random_state=42),
    "SVM": SVC(probability=True, random_state=42),
    "K-Nearest Neighbors": KNeighborsClassifier(),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
}

results = []
for model_name, model in models.items():
    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring="roc_auc")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else None

    accuracy = accuracy_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_proba) if y_proba is not None else None

    results.append({
        "Model": model_name,
        "Accuracy": accuracy,
        "ROC-AUC": roc_auc,
        "CV Mean ROC-AUC": cv_scores.mean(),
        "CV Std ROC-AUC": cv_scores.std(),
    })

    print(f"\n=== {model_name} ===")
    print(classification_report(y_test, y_pred))

results_df = pd.DataFrame(results)

# Get best model based on CV mean ROC-AUC
best_model = results_df.loc[results_df["CV Mean ROC-AUC"].idxmax()]

print("\n=== Model Comparison ===")
print(results_df)

print("\n=== Best Model ===")
print(best_model)

results_melted = results_df.melt(id_vars="Model", var_name="Metric", value_name="Score")
plt.figure(figsize=(10, 6))
sns.barplot(data=results_melted, x="Model", y="Score", hue="Metric")
plt.title("Model Performance Comparison")
plt.ylabel("Scores")
plt.xticks(rotation=45)
plt.show()

best_model_name = best_model["Model"]
best_model_instance = models[best_model_name]
y_pred_best = best_model_instance.predict(X_test)
conf_matrix = confusion_matrix(y_test, y_pred_best)

plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", cbar=True)
plt.title(f"Confusion Matrix: {best_model_name}")
plt.xlabel("Predicted Labels")
plt.ylabel("True Labels")
plt.show()
