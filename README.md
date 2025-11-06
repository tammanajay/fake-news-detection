# Fake News Detection (College Mini Project)

A simple machine learning project that predicts whether a news article is real or fake.
This was built as part of my college coursework to understand text processing and integrating ML models into a simple web app. The goal was not to build the most advanced model, but to learn the end-to-end workflow, i.e., from data to model to deployment.

## Technology Stack
- Python
- scikit-learn
- TF-IDF for text features
- Logistic Regression
- Django for a small web interface

## How It Works
1. The user enters text input (a news headline or statement)
2. The text is converted into numerical features using TF-IDF
3. Logistic Regression predicts whether it's real or fake
4. The result is shown on a simple web page
