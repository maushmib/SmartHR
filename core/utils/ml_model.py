import pickle, os
from sklearn.feature_extraction.text import TfidfVectorizer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = pickle.load(open(os.path.join(BASE_DIR, "resume_model.pkl"), "rb"))
vectorizer = pickle.load(open(os.path.join(BASE_DIR, "vectorizer.pkl"), "rb"))

def predict_resume(text):
    features = vectorizer.transform([text])
    prediction = model.predict(features)[0]
    return "Real" if prediction == 1 else "Fake"
