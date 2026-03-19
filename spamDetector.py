import joblib

# Load saved model
model = joblib.load("./assets/model.pkl")
vectorizer = joblib.load("./assets/vectorizer.pkl")


def checkStatus(msg):
    msg_vec = vectorizer.transform([msg])
    prediction = model.predict(msg_vec)

    if msg == "" or prediction[0] == 1 or prediction[0] == 2:
        return "Spam"
    else:
        return "Not Spam"
