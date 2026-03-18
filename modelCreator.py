import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import joblib

# 1️⃣ Load CSV
df = pd.read_csv("./assets/df.csv")   # change filename if needed

df["text"] = df["text"].fillna("")
df["text"] = df["text"].astype(str)

# 2️⃣ Split data into input and output
X = df["text"]
y = df["label"]

# 3️⃣ Train-Test split
# X_train, X_test, y_train, y_test = train_test_split(
#     X, y, test_size=0.2, random_state=42
# )

# 4️⃣ Convert text into numbers
vectorizer = CountVectorizer()
# X_train_vec = vectorizer.fit_transform(X_train)
# X_test_vec = vectorizer.transform(X_test)
X_vec = vectorizer.fit_transform(X)

# 5️⃣ Train model
# model = MultinomialNB()
# model.fit(X_train_vec, y_train)

# # 6️⃣ Check accuracy
# accuracy = model.score(X_test_vec, y_test)
# print("Accuracy:", accuracy)

# # 7️⃣ Test your own message
# msg = ["Congratulations! You won ₹50000"]
# msg_vec = vectorizer.transform(msg)
# prediction = model.predict(msg_vec)

actualModel = MultinomialNB()
actualModel.fit(X_vec, y)

joblib.dump(actualModel, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

# if prediction[0] == 1 or prediction[0] == 2:
#     print("Spam")
# else:
#     print("Not Spam")
