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