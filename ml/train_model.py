import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib

# Dataset de exemplo
data = {
    "log": ["Error 404 Not Found", "500 Internal Server Error", "200 OK"],
    "label": ["error", "error", "ok"]
}
df = pd.DataFrame(data)

# Vetorização
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df["log"])
y = df["label"]

# Treinamento
model = MultinomialNB()
model.fit(X, y)

# Salvar modelo
joblib.dump(model, "error_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")
print("Modelo treinado e salvo!")
