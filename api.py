from fastapi import FastAPI
import joblib

# Create API
app = FastAPI(
    title="AI Fake Job & Internship Detector API",
    description="API for estimating the fraud risk of job and internship postings.",
    version="1.0"
)

# Load trained ML model and TF-IDF vectorizer
model = joblib.load("model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")


@app.get("/")
def home():
    return {
        "message": "AI Fake Job & Internship Detector API is running"
    }


@app.post("/analyze")
def analyze_job(job_text: str):

    # Check empty input
    if not job_text.strip():
        return {
            "error": "Please enter a job or internship description."
        }

    # Convert text into TF-IDF features
    job_tfidf = vectorizer.transform([job_text])

    # ML prediction
    prediction = model.predict(job_tfidf)[0]

    # Model-estimated risk score
    fraud_probability = model.predict_proba(job_tfidf)[0][1]
    risk_score = fraud_probability * 100

    # Risk level
    if risk_score < 30:
        risk_level = "Low Risk"
    elif risk_score < 70:
        risk_level = "Medium Risk"
    else:
        risk_level = "High Risk"

    # Prediction result
    if prediction == 1:
        result = "Potentially Fraudulent Job"
    else:
        result = "Likely Legitimate Job"

    # Suspicious indicators
    suspicious_indicators = []

    text = job_text.lower()

    if any(word in text for word in [
        "registration fee",
        "pay money",
        "upfront payment",
        "payment required"
    ]):
        suspicious_indicators.append("Payment Request")

    if any(word in text for word in [
        "earn huge money",
        "guaranteed income",
        "make money fast"
    ]):
        suspicious_indicators.append("Unrealistic Salary/Earnings")

    if any(word in text for word in [
        "urgent hiring",
        "apply immediately",
        "limited seats"
    ]):
        suspicious_indicators.append("Urgency")

    if any(word in text for word in [
        "bank details",
        "credit card",
        "send your password"
    ]):
        suspicious_indicators.append("Personal Information Request")

    return {
        "risk_score": round(risk_score, 2),
        "risk_level": risk_level,
        "prediction": result,
        "suspicious_indicators": suspicious_indicators
    }