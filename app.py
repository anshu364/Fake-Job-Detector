import streamlit as st
import joblib


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Fake Job Detector",
    page_icon="🔍",
    layout="centered"
)


# --------------------------------------------------
# Load Model and TF-IDF Vectorizer
# --------------------------------------------------

model = joblib.load("model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")


# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("🔍 AI Fake Job & Internship Detector")

st.write(
    "Analyze a job or internship posting and estimate its potential fraud risk."
)

st.divider()


# --------------------------------------------------
# Job Posting Input
# --------------------------------------------------

st.subheader("📄 Enter Job Posting")

job_text = st.text_area(
    "Paste the job description here:",
    height=250,
    placeholder="Paste the complete job or internship description..."
)


# --------------------------------------------------
# Analyze Button
# --------------------------------------------------

if st.button("🔎 Analyze Job", use_container_width=True):

    if job_text.strip() == "":
        st.warning("⚠️ Please enter a job posting first.")

    else:

        # --------------------------------------------------
        # Convert Job Text into TF-IDF
        # --------------------------------------------------

        job_tfidf = vectorizer.transform([job_text])


        # --------------------------------------------------
        # Model Prediction
        # --------------------------------------------------

        prediction = model.predict(job_tfidf)[0]

        fraud_probability = model.predict_proba(job_tfidf)[0][1]

        risk_score = fraud_probability * 100


        # --------------------------------------------------
        # Analysis Result
        # --------------------------------------------------

        st.divider()

        st.subheader("📊 Analysis Result")

        st.metric(
            "Model-Estimated Risk Score",
            f"{risk_score:.2f}%"
        )


        # --------------------------------------------------
        # Risk Level
        # --------------------------------------------------

        if risk_score < 30:
            risk_level = "🟢 Low Risk"

        elif risk_score < 70:
            risk_level = "🟡 Medium Risk"

        else:
            risk_level = "🔴 High Risk"


        st.write("### Risk Level")

        st.write(risk_level)


        # --------------------------------------------------
        # Prediction Result
        # --------------------------------------------------

        if prediction == 1:

            st.error(
                "⚠️ Potentially Fraudulent Job"
            )

        else:

            st.success(
                "✅ Likely Legitimate Job"
            )


        # --------------------------------------------------
        # Suspicious Keywords
        # --------------------------------------------------

        # --------------------------------------------------
# Suspicious Keywords
# --------------------------------------------------

suspicious_keywords = {

    "Payment Request": [
        "registration fee",
        "pay money",
        "upfront payment",
        "payment required"
    ],

    "Unrealistic Salary": [
        "earn huge money",
        "guaranteed income",
        "make money fast"
    ],

    "Urgency": [
        "urgent hiring",
        "apply immediately",
        "limited seats"
    ],

    "Personal Information": [
        "bank details",
        "credit card",
        "send your password"
    ]
}


# --------------------------------------------------
# Find Suspicious Indicators
# --------------------------------------------------

found_indicators = []

job_text_lower = job_text.lower()


for category, keywords in suspicious_keywords.items():

    for keyword in keywords:

        if keyword not in job_text_lower:
            continue

        # Sentences that clearly deny the suspicious action
        denial_phrases = [
            "no " + keyword,
            "no any " + keyword,
            "not " + keyword,
            "without " + keyword,
            "without any " + keyword,
            "does not require " + keyword,
            "do not require " + keyword,
            "is not required",
            "are not required"
        ]

        # Special cases for payment/fee denial
        payment_denial_phrases = [
            "no payment",
            "no registration fee",
            "no payment or registration fee",
            "no registration fee or payment",
            "no payment is required",
            "no payment required",
            "no fee is required",
            "no fees are required",
            "no fees required",
            "without payment",
            "without any payment"
        ]

        is_denied = any(
            phrase in job_text_lower
            for phrase in denial_phrases
        )

        if category == "Payment Request":

            if any(
                phrase in job_text_lower
                for phrase in payment_denial_phrases
            ):
                is_denied = True

        if not is_denied:

            found_indicators.append(
                (category, keyword)
            )


# --------------------------------------------------
# Display Suspicious Indicators
# --------------------------------------------------

if found_indicators:

    st.subheader("⚠️ Possible Suspicious Indicators")

    for category, keyword in found_indicators:

        st.warning(
            f"**{category}:** {keyword}"
        )

else:

    st.subheader("✅ Suspicious Indicators")

    st.success(
        "No obvious suspicious keywords detected."
    )


st.divider()
       
        
        