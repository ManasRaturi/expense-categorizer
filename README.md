# Expense Auto-Categorizer

A machine learning tool that automatically categorizes expense descriptions from a CSV file into meaningful spending categories — like Food, Transport, Shopping, Health, and more.

## Problem Statement

Manually reviewing bank statements or UPI transaction histories to understand your spending is tedious and time-consuming. Descriptions like "Swiggy order", "Uber ride", or "Apollo pharmacy" clearly belong to specific categories, but doing this by hand for hundreds of rows is impractical.

This project trains a text classifier that reads expense descriptions and automatically assigns each one to the correct spending category — turning a raw CSV into a structured, analysable spending report.

## How It Works

1. **Training Data** — A labelled dataset of common Indian expense descriptions across 8 categories is used to train the model.
2. **Preprocessing** — Descriptions are lowercased, cleaned, stopwords removed, and stemmed.
3. **TF-IDF Vectorization** — Text is converted to numerical features using TF-IDF with unigrams and bigrams.
4. **Logistic Regression Classifier** — A multi-class Logistic Regression model predicts the category with a probability score.
5. **Automation** — The CLI accepts any CSV, auto-detects the description column, classifies every row, and outputs an enriched CSV with a `category` column added.

## Categories

| Emoji | Category |
|-------|----------|
| 🍔 | Food & Dining |
| 🚗 | Transport |
| 🛍️ | Shopping |
| 🎬 | Entertainment |
| 💊 | Health |
| 📚 | Education |
| 💡 | Utilities & Bills |
| ✈️ | Travel & Stays |

## Project Structure

```
expense-categorizer/
├── data/
│   ├── training_data.csv      # Labelled training examples (generated)
│   └── my_expenses.csv        # Sample expenses CSV (generated)
├── model/
│   └── pipeline.pkl           # Saved model pipeline (generated after training)
├── generate_data.py           # Generates training data and sample CSV
├── train.py                   # Trains and saves the model
├── categorize.py              # Core prediction module (importable)
├── app.py                     # Command-line interface
├── requirements.txt
└── README.md
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/ManasRaturi/expense-categorizer.git
cd expense-categorizer
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Generate Training Data

```bash
python generate_data.py
```

This creates:
- `data/training_data.csv` — 160 labelled examples across 8 categories
- `data/my_expenses.csv` — 30 sample expense rows to test on

### 5. Train the Model

```bash
python train.py
```

This prints cross-validation accuracy and saves the model to `model/pipeline.pkl`.

**Expected accuracy: ~95–98%**

### 6. Run the App

**Categorize your CSV (with spending summary):**
```bash
python app.py --file data/my_expenses.csv --summary
```

**Run built-in demo:**
```bash
python app.py --demo
```

**Classify a single description:**
```bash
python app.py --desc "Swiggy biryani order"
```

**Categorize and save output to a new CSV:**
```bash
python app.py --file data/my_expenses.csv --summary --save
```

**Specify the description column manually:**
```bash
python app.py --file your_bank_statement.csv --col narration --summary
```

**Interactive mode:**
```bash
python app.py
```

## Example Output

```
  #    Description                         Category               Conf
  ──────────────────────────────────────────────────────────────────────
  1    Swiggy biryani order                🍔 Food & Dining        97.3%
  2    Uber ride to college                🚗 Transport            96.1%
  3    Amazon headphones                   🛍️ Shopping             94.8%
  4    Netflix monthly plan                🎬 Entertainment        98.2%
  5    Pharmacy paracetamol                💊 Health               95.5%

  ── SPENDING SUMMARY ──────────────────────────────────────────
  Category                  Txns      Amount    Share
  ─────────────────────────────────────────────────────────────
  🍔 Food & Dining             8    ₹  3,260    21.4%  ████
  🛍️ Shopping                  5    ₹  5,947    39.1%  ███████
  🎬 Entertainment             4    ₹  1,437     9.4%  █
  ...
```

## Using With Your Own Bank Statement

Export your UPI/bank transaction history as a CSV. The app will auto-detect the description column. If it fails, specify it manually:

```bash
python app.py --file my_bank.csv --col narration --summary --save
```

## Course Concepts Applied

- Text preprocessing (tokenisation, stemming, stopword removal)
- TF-IDF feature extraction with n-grams
- Logistic Regression for multi-class classification
- sklearn Pipeline for clean train/predict workflow
- Cross-validation for robust model evaluation
- Model serialisation with `pickle`
- CLI automation with `argparse`

## Author

Manas Raturi  
Reg. No.: 25BAS10041  
VIT Bhopal University
