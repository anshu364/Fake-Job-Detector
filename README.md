# 🔍 AI Fake Job & Internship Detector

An AI/ML-based application that analyzes job and internship postings and estimates their potential fraud risk.

The project combines **Natural Language Processing (NLP)**, **TF-IDF**, **Machine Learning**, and **rule-based suspicious indicator detection** to help students and job seekers identify potentially risky postings.

---

## 🎯 Project Objective

Fake job and internship postings can target students and job seekers through misleading salaries, payment requests, urgency, or requests for sensitive information.

The objective of this project is to build an AI-based system that:

- Analyzes job posting text
- Predicts whether a posting is likely legitimate or potentially fraudulent
- Provides a model-estimated risk score
- Classifies the posting into Low, Medium, or High Risk
- Highlights possible suspicious indicators

> ⚠️ The system provides a risk assessment and does not prove that a job posting is fraudulent.

---

## ⚙️ How It Works

```text
Job Posting
     ↓
Text Cleaning
     ↓
TF-IDF Feature Extraction
     ↓
Logistic Regression Model
     ↓
Risk Score
     ↓
Risk Level
     ↓
Suspicious Indicators
---

## 🧠 Machine Learning Model

The project uses **TF-IDF (Term Frequency-Inverse Document Frequency)** to convert job posting text into numerical features.

A **Logistic Regression** classifier is then used to predict whether the posting is potentially fraudulent or likely legitimate.

### Model Configuration

- Dataset: Real/Fake Job Posting Dataset
- Total Job Postings: 17,880
- TF-IDF Features: 5,000
- Train-Test Split: 80/20
- Class Balancing: `class_weight="balanced"`
- Model: Logistic Regression

### Model Performance

- Accuracy: 96.76%
- Fraudulent Class Precision: 61%
- Fraudulent Class Recall: 90%
- Fraudulent Class F1-Score: 73%

> Note: The risk score is a model-estimated score and should not be interpreted as a calibrated real-world probability.

---

## 📱 Application

The project is available through:

- **Streamlit Web Application** for testing job postings
- **FastAPI Backend** for serving ML predictions
- **Android Application** built using Kotlin and Android Studio
- **Render** for online API deployment

### System Architecture

```text
Job Posting
     ↓
Text Preprocessing
     ↓
TF-IDF Vectorization
     ↓
Logistic Regression
     ↓
Fraud Prediction
     ↓
Risk Score
     ↓
Risk Level
     ↓
Suspicious Indicators
     ↓
FastAPI
     ↓
Android Application
