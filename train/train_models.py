import os
import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

DATA_PATH = "data/emotions_dataset.csv"
MODELS_DIR = "models"

os.makedirs(MODELS_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH)

X = df["text"].astype(str)
y_sentiment = df["sentiment"].astype(str)
y_emotion = df["emotion"].astype(str)

vectorizer = TfidfVectorizer(
    ngram_range=(1, 3),
    lowercase=True,
    strip_accents="unicode"
)

X_vec = vectorizer.fit_transform(X)

sentiment_model = LogisticRegression(max_iter=2000, class_weight="balanced")
emotion_model = LogisticRegression(max_iter=2000, class_weight="balanced")

sentiment_model.fit(X_vec, y_sentiment)
emotion_model.fit(X_vec, y_emotion)

joblib.dump(vectorizer, os.path.join(MODELS_DIR, "vectorizer.joblib"))
joblib.dump(sentiment_model, os.path.join(MODELS_DIR, "sentiment_model.joblib"))
joblib.dump(emotion_model, os.path.join(MODELS_DIR, "emotion_model.joblib"))

print("✅ Models trained and saved successfully.")git --version