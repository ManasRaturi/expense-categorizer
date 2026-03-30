"""
train.py - Train the Expense Categorizer model
Run this after generate_data.py to train and save the classifier.
Usage: python train.py
"""

import os
import pickle
import pandas as pd
import nltk
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re

nltk.download('stopwords', quiet=True)

ps         = PorterStemmer()
stop_words = set(stopwords.words('english'))

TRAINING_DATA_PATH = os.path.join('data', 'training_data.csv')
MODEL_PATH         = os.path.join('model', 'pipeline.pkl')


def preprocess(text: str) -> str:
    text   = text.lower()
    text   = re.sub(r'[^a-z\s]', '', text)
    tokens = [ps.stem(t) for t in text.split() if t not in stop_words]
    return ' '.join(tokens)


# ── Load training data ────────────────────────────────────────────────────────

print(f"Loading training data from '{TRAINING_DATA_PATH}' ...")
try:
    df = pd.read_csv(TRAINING_DATA_PATH)
except FileNotFoundError:
    print("\n[ERROR] Training data not found. Run 'python generate_data.py' first.")
    raise SystemExit(1)

df['clean'] = df['description'].apply(preprocess)
print(f"Loaded {len(df)} labelled examples across {df['category'].nunique()} categories.\n")
print("Categories found:")
for cat, count in df['category'].value_counts().items():
    print(f"  {cat:<25} {count} examples")

# ── Build sklearn Pipeline ────────────────────────────────────────────────────

pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(
        max_features=3000,
        ngram_range=(1, 2),
        sublinear_tf=True,
    )),
    ('clf', LogisticRegression(
        max_iter=1000,
        C=5.0,
        solver='lbfgs',
        multi_class='multinomial',
    )),
])

# ── Cross-validation ──────────────────────────────────────────────────────────

print("\nRunning 5-fold cross-validation...")
cv_scores = cross_val_score(pipeline, df['clean'], df['category'], cv=5, scoring='accuracy')
print(f"CV Accuracy: {cv_scores.mean()*100:.2f}% ± {cv_scores.std()*100:.2f}%")

# ── Train on full data, evaluate on held-out split ────────────────────────────

X_train, X_test, y_train, y_test = train_test_split(
    df['clean'], df['category'], test_size=0.2, random_state=42, stratify=df['category']
)

pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)

print("\n" + "="*60)
print("            MODEL EVALUATION RESULTS")
print("="*60)
print(f"Held-out Accuracy : {accuracy_score(y_test, y_pred)*100:.2f}%")
print("\nPer-Category Report:")
print(classification_report(y_test, y_pred))
print("="*60)

# ── Retrain on ALL data and save ──────────────────────────────────────────────

pipeline.fit(df['clean'], df['category'])   # use every labelled example

os.makedirs('model', exist_ok=True)
with open(MODEL_PATH, 'wb') as f:
    pickle.dump(pipeline, f)

print(f"\nFull pipeline saved → {MODEL_PATH}")
print("You can now run:  python app.py --file data/my_expenses.csv")
