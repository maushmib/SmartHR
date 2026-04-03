import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from imblearn.over_sampling import SMOTE
import joblib
import os

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, 'attrition_data_engineering.csv')

# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv(csv_path)

# Encode Attrition
df['Attrition'] = df['Attrition'].map({"No": 0, "Yes": 1})

# -----------------------------
# Feature engineering
# -----------------------------
# Salary vs Role Avg
role_avg_salary = df.groupby('JobRole')['MonthlyIncome'].transform('mean')
df['Salary_vs_Role_Avg'] = df['MonthlyIncome'] / role_avg_salary

# Select features
selected_features = ['Age', 'Gender', 'Education', 'EducationField', 'JobRole', 
                     'MonthlyIncome', 'Salary_vs_Role_Avg']
df = df[selected_features + ['Attrition']]

# One-hot encode categorical
df = pd.get_dummies(df, columns=['Gender', 'EducationField', 'JobRole'], drop_first=True)

# -----------------------------
# Features and target
# -----------------------------
X = df.drop('Attrition', axis=1)
y = df['Attrition']

# -----------------------------
# Scale numeric features
# -----------------------------
numeric_cols = ['Age', 'MonthlyIncome', 'Education', 'Salary_vs_Role_Avg']
scaler = StandardScaler()
X[numeric_cols] = scaler.fit_transform(X[numeric_cols])

# -----------------------------
# Handle class imbalance
# -----------------------------
smote = SMOTE(random_state=42)
X_res, y_res = smote.fit_resample(X, y)

# -----------------------------
# Train-validation-test split
# -----------------------------
X_temp, X_test, y_temp, y_test = train_test_split(X_res, y_res, test_size=0.2, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.25, random_state=42)
# 60% train / 20% val / 20% test

# -----------------------------
# Train RandomForest with controlled overfitting
# -----------------------------
model = RandomForestClassifier(
    n_estimators=500,
    max_depth=20,           # limit tree depth
    min_samples_leaf=3,     # minimum samples per leaf
    max_features='sqrt',
    random_state=42,
    class_weight='balanced'
)
model.fit(X_train, y_train)

# -----------------------------
# Evaluate model
# -----------------------------
y_train_pred = model.predict(X_train)
y_val_pred = model.predict(X_val)
y_test_pred = model.predict(X_test)

print(f"🎯 Training Accuracy: {accuracy_score(y_train, y_train_pred) * 100:.2f}%")
print(f"🎯 Validation Accuracy: {accuracy_score(y_val, y_val_pred) * 100:.2f}%")
print(f"🎯 Test Accuracy: {accuracy_score(y_test, y_test_pred) * 100:.2f}%\n")

print("Classification Report (Test Set):\n")
print(classification_report(y_test, y_test_pred))

print("Confusion Matrix (Test Set):\n")
print(confusion_matrix(y_test, y_test_pred))

# Feature importance
importances = model.feature_importances_
feature_names = X_train.columns
sorted_features = sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True)
print("\n📊 Feature Importances:")
for feature, importance in sorted_features:
    print(f"{feature}: {importance:.4f}")

# -----------------------------
# Save everything
# -----------------------------
joblib.dump(model, os.path.join(BASE_DIR, 'attrition_model.pkl'))
joblib.dump(scaler, os.path.join(BASE_DIR, 'scaler.pkl'))
joblib.dump(list(X.columns), os.path.join(BASE_DIR, 'model_features.pkl'))

print("\n✅ Model trained with controlled overfitting and ready for realistic predictions.")
