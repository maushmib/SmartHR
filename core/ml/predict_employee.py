import pandas as pd
import joblib
import os

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'attrition_model.pkl')
scaler_path = os.path.join(BASE_DIR, 'scaler.pkl')
features_path = os.path.join(BASE_DIR, 'model_features.pkl')
training_data_path = os.path.join(BASE_DIR, 'attrition_data_engineering.csv')  # for role averages

# -----------------------------
# Load model and scaler
# -----------------------------
model = joblib.load(model_path)
scaler = joblib.load(scaler_path)
model_features = joblib.load(features_path)

# -----------------------------
# Load training data for role averages
# -----------------------------
train_df = pd.read_csv(training_data_path)
role_avg_salary_train = train_df.groupby('JobRole')['MonthlyIncome'].mean().to_dict()

# -----------------------------
# Example new employee data
# -----------------------------
new_data = [
    {"Employee Name": "e1", "Age": 23, "Gender": "Male", "Education": 2,
     "EducationField": "Computer Science", "JobRole": "Junior Developer", "MonthlyIncome": 90000},
    {"Employee Name": "e2", "Age": 35, "Gender": "Female", "Education": 4,
     "EducationField": "Information Technology", "JobRole": "Software Engineer", "MonthlyIncome": 95000},
    {"Employee Name": "e3", "Age":60, "Gender": "Female", "Education": 2,
     "EducationField": "Electronics", "JobRole": "QA Engineer", "MonthlyIncome": 10000},
]

df = pd.DataFrame(new_data)

# -----------------------------
# Feature engineering
# -----------------------------
# Use training role averages
df['Salary_vs_Role_Avg'] = df.apply(
    lambda row: row['MonthlyIncome'] / role_avg_salary_train.get(row['JobRole'], row['MonthlyIncome']),
    axis=1
)

# One-hot encode categorical to match training features
df_encoded = pd.get_dummies(df, columns=['Gender','EducationField','JobRole'], drop_first=True)

# Add missing columns with 0
for col in model_features:
    if col not in df_encoded.columns:
        df_encoded[col] = 0

# Ensure correct column order
df_encoded = df_encoded[model_features]

# Scale numeric features
numeric_cols = ['Age', 'MonthlyIncome', 'Education', 'Salary_vs_Role_Avg']
df_encoded[numeric_cols] = scaler.transform(df_encoded[numeric_cols])

# -----------------------------
# Predict with probability threshold
# -----------------------------
probs = model.predict_proba(df_encoded)[:,1]
threshold = 0.35
y_pred = (probs > threshold).astype(int)

# -----------------------------
# Rule-based override for extreme low salary
# -----------------------------
salary_threshold = 0.5  # below 50% of role average is high risk
final_pred = []
for p, svra in zip(y_pred, df['Salary_vs_Role_Avg']):
    if p == 1 or svra < salary_threshold:
        final_pred.append('🚨 Likely to Leave')
    else:
        final_pred.append('✅ Likely to Stay')

df['Attrition Prediction'] = final_pred
df['Attrition Probability'] = probs.round(2)

# -----------------------------
# Show results
# -----------------------------
print(df[['Employee Name','JobRole','MonthlyIncome','Salary_vs_Role_Avg','Attrition Probability','Attrition Prediction']])
