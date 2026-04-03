import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load data from train.csv (ensure train.csv is in the same directory)
df = pd.read_csv('train.csv')

# Features and target (ensure these columns exist in your CSV)
X = df[['tasks_left', 'deadline_days', 'project_criticality']]
y = df['safe_to_approve']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Save model in the same directory as this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'leave_model.pkl')
joblib.dump(model, model_path)
print(f"Model saved at: {model_path}")
