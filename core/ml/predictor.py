import joblib
import re

# Load saved model + vectorizer
model = joblib.load("ml/resume_model.pkl")
vectorizer = joblib.load("ml/resume_vectorizer.pkl")

def clean_text(text):
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    text = text.lower()
    return text

def predict_resume(resume_text):
    cleaned = clean_text(resume_text)
    vectorized = vectorizer.transform([cleaned])
    prediction = model.predict(vectorized)[0]
    return "Real" if prediction == 1 else "Fake"
