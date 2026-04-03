import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib

# 1️⃣ Load dataset
df = pd.read_csv("UpdatedResumeDataSet.csv/UpdatedResumeDataSet.csv")

# 2️⃣ Preprocess text
def clean_text(text):
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    text = text.lower()
    return text

df['cleaned_resume'] = df['Resume'].apply(clean_text)

# 3️⃣ Simple binary label
df['label'] = df['Category'].apply(lambda x: 1 if x in ['Data Science','HR','Designing'] else 0)

# 4️⃣ Train, Validation, Test Split
X_temp, X_test, y_temp, y_test = train_test_split(df['cleaned_resume'], df['label'], test_size=0.2, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.25, random_state=42)  # 0.25*0.8 = 0.2

# 5️⃣ TF-IDF Vectorizer
vectorizer = TfidfVectorizer(max_features=5000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_val_tfidf = vectorizer.transform(X_val)
X_test_tfidf = vectorizer.transform(X_test)

# 6️⃣ Logistic Regression Model
model = LogisticRegression()
model.fit(X_train_tfidf, y_train)

# 7️⃣ Evaluate Accuracy
y_train_pred = model.predict(X_train_tfidf)
y_val_pred = model.predict(X_val_tfidf)
y_test_pred = model.predict(X_test_tfidf)

print("Training Accuracy:", accuracy_score(y_train, y_train_pred))
print("Validation Accuracy:", accuracy_score(y_val, y_val_pred))
print("Test Accuracy:", accuracy_score(y_test, y_test_pred))

# 8️⃣ Save Model & Vectorizer
joblib.dump(model, "resume_model.pkl")
joblib.dump(vectorizer, "resume_vectorizer.pkl")
print("✅ Resume model and vectorizer saved.")
