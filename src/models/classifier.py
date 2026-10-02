import joblib

from preprocessing.preprocess import preprocess_resume


model = joblib.load("models/trained_models/svm_model.pkl")
vectorizer = joblib.load("models/vectorizers/tfidf_vectorizer.pkl")
encoder = joblib.load("models/encoders/label_encoder.pkl")


def predict_resume_category(resume_text):

    cleaned_resume = preprocess_resume(resume_text)

    vector = vectorizer.transform([cleaned_resume])

    prediction = model.predict(vector)

    return encoder.inverse_transform(prediction)[0]