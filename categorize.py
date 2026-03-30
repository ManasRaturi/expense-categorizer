"""
categorize.py - Core prediction module
Loads the saved pipeline and exposes categorize() and categorize_csv().
"""

import os
import pickle
import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

nltk.download('stopwords', quiet=True)

MODEL_PATH = os.path.join('model', 'pipeline.pkl')

ps         = PorterStemmer()
stop_words = set(stopwords.words('english'))

CATEGORY_EMOJI = {
    "Food & Dining":    "🍔",
    "Transport":        "🚗",
    "Shopping":         "🛍️",
    "Entertainment":    "🎬",
    "Health":           "💊",
    "Education":        "📚",
    "Utilities & Bills":"💡",
    "Travel & Stays":   "✈️",
}


def _load_pipeline():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            "Model not found. Please run 'python train.py' first."
        )
    with open(MODEL_PATH, 'rb') as f:
        return pickle.load(f)


def _preprocess(text: str) -> str:
    text   = text.lower()
    text   = re.sub(r'[^a-z\s]', '', text)
    tokens = [ps.stem(t) for t in text.split() if t not in stop_words]
    return ' '.join(tokens)


def categorize(description: str) -> dict:
    """
    Predict the expense category for a single description string.

    Returns dict with:
        category    – predicted category name
        emoji       – emoji for the category
        confidence  – confidence % of top prediction
        top3        – list of (category, confidence%) for top 3 predictions
    """
    pipeline = _load_pipeline()
    clean    = _preprocess(description)
    proba    = pipeline.predict_proba([clean])[0]
    classes  = pipeline.classes_

    top_indices = proba.argsort()[::-1]
    top3 = [(classes[i], round(proba[i] * 100, 1)) for i in top_indices[:3]]

    category   = top3[0][0]
    confidence = top3[0][1]

    return {
        'category':   category,
        'emoji':      CATEGORY_EMOJI.get(category, '📦'),
        'confidence': confidence,
        'top3':       top3,
    }


def categorize_csv(input_path: str, desc_column: str = None) -> pd.DataFrame:
    """
    Read a CSV, auto-detect or use the specified description column,
    classify every row, and return an enriched DataFrame.
    """
    pipeline = _load_pipeline()

    df = pd.read_csv(input_path)

    # ── Auto-detect description column ───────────────────────────────────────
    if desc_column is None:
        candidates = ['description', 'desc', 'details', 'narration',
                      'particulars', 'merchant', 'name', 'item', 'note']
        for col in candidates:
            for actual in df.columns:
                if col in actual.lower():
                    desc_column = actual
                    break
            if desc_column:
                break
        if desc_column is None:
            # fall back to first text column
            for col in df.columns:
                if df[col].dtype == object:
                    desc_column = col
                    break

    if desc_column is None:
        raise ValueError("Could not find a text column to classify. "
                         "Use --col to specify the column name.")

    print(f"  Using column '{desc_column}' for classification.")

    cleaned = df[desc_column].fillna('').apply(_preprocess)
    df['category']   = pipeline.predict(cleaned)
    df['confidence'] = [
        round(max(pipeline.predict_proba([c])[0]) * 100, 1)
        for c in cleaned
    ]
    df['emoji'] = df['category'].map(CATEGORY_EMOJI).fillna('📦')

    return df, desc_column
