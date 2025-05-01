
# import pickle
# # from sklearn.feature_extraction.text import TfidfVectorizer
# import joblib
# import sklearn
# from tensorflow.keras.models import load_model
# print(sklearn.__version__)

# vectorizer = joblib.load('api/model_weights/DNN/tfidf_vectorizer.pkl')

# loaded_model = load_model('api/model_weights/DNN/ann_model.h5')


# def analyze_url(url):
#     try:
#         print(hasattr(vectorizer, "idf_"))
#         print(vectorizer)
#         print(url)
#         # Preprocess the URL
#         url_transformed = vectorizer.transform([url])
#         # Make a prediction
#         prediction = loaded_model.predict(url_transformed)
#         print(prediction)
#         y_pred = prediction[0][0] < 0.5
#         return {"is_phishing": y_pred, "confidence": prediction[0][0], "success": True, "error": ""}
#     except Exception as e:
#         print(e)
#         return {"is_phishing": "", "confidence": -1, "success": False, "error": str(e)}

import re
import os
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Use BASE_DIR from settings (points to the project root)
from django.conf import settings
BASE_DIR = settings.BASE_DIR

# Construct absolute paths to model and tokenizer
model_path = os.path.join(BASE_DIR, 'rnn_model',
                          'bidirectional_rnn_url_classifier.h5')
tokenizer_path = os.path.join(BASE_DIR, 'rnn_model', 'tokenizer.pkl')

# Load the trained RNN model
loaded_model = load_model(model_path)
print("[INFO] Bidirectional RNN model loaded.")

# Load the tokenizer
with open(tokenizer_path, 'rb') as f:
    loaded_tokenizer = pickle.load(f)
print("[INFO] Tokenizer loaded.")

# model_path = os.path.join(BASE_DIR, 'rnn_model', 'rnn_model.h5')
# tokenizer_path = os.path.join(BASE_DIR, 'rnn_model', 'tokenizer.pkl')

# loaded_model = load_model(
#     "api/model_weights/RNN/bidirectional_rnn_url_classifier.h5")
# print("[INFO] Bidirectional RNN model loaded.")


# # Load tokenizer
# with open("api/model_weights/RNN/tokenizer.pkl", "rb") as f:
#     loaded_tokenizer = pickle.load(f)
# print("[INFO] Tokenizer loaded.")


def normalize_url(url):
    url = url.lower()
    url = re.sub(r'^https?:\/\/', '', url)
    url = url.strip().strip('/')
    return url


def analyze_url(url, model=loaded_model, tokenizer=loaded_tokenizer, max_len=200):
    try:
        print(f"[INFO] Input URL: {url}")

        # Normalize and tokenize
        cleaned_url = normalize_url(url)
        sequence = tokenizer.texts_to_sequences([cleaned_url])
        padded_input = pad_sequences(sequence, maxlen=max_len, padding='post')

        # Predict
        prediction = model.predict(padded_input)
        confidence = float(prediction[0][0])
        is_phishing = confidence < 0.5

        print(f"[INFO] Prediction: {prediction} → Phishing: {is_phishing}")

        return {
            "is_phishing": is_phishing,
            "confidence": confidence,
            "success": True,
            "error": ""
        }
    except Exception as e:
        print("[ERROR]", e)
        return {
            "is_phishing": "",
            "confidence": -1,
            "success": False,
            "error": str(e)
        }
