import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


# Load cleaned dataset
df = pd.read_csv("data/cleaned_jobs.csv")

# Separate text and target
X_text = df["combined_text"]
y = df["fraudulent"]


# Split data
X_train_text, X_test_text, y_train, y_test = train_test_split(
    X_text,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# TF-IDF
vectorizer = TfidfVectorizer(
    max_features=5000,
    stop_words="english"
)

X_train = vectorizer.fit_transform(X_train_text)


# Logistic Regression model
model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced"
)


# Train model
model.fit(X_train, y_train)


# Save model and vectorizer
joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")

print("Model and vectorizer saved successfully!")