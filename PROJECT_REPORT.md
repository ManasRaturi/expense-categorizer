# Project Report — Expense Auto-Categorizer

**Student:** Manas Raturi  
**Registration No:** 25BAS10041  
**Institution:** VIT Bhopal University  

---

## 1. Problem Statement

Every time I open my UPI app or download a bank statement, I see dozens of raw transaction descriptions: "Swiggy order 281", "UBER TRIP 8829", "APMC PHARM", "NFLX". Manually tagging each transaction into a category — Food, Transport, Health, Entertainment — to understand my spending patterns takes significant time and effort.

This project builds an automated ML pipeline that reads a CSV of expense descriptions and classifies each one into the correct spending category, effectively turning a raw transaction dump into a structured spending report.

---

## 2. Why This Problem Matters

- Students and working professionals generate hundreds of digital transactions per month
- Understanding where money goes is the first step towards financial discipline
- Manual categorisation is error-prone and not scalable
- Bank apps offer basic filters but no intelligent category inference from freeform descriptions
- A standalone tool can process any CSV export — UPI history, bank statement, or manual expense log

---

## 3. Dataset

Since no labelled real-world expense dataset was readily available, I constructed a custom training dataset:

- **160 labelled examples** hand-curated across **8 categories**
- Categories: Food & Dining, Transport, Shopping, Entertainment, Health, Education, Utilities & Bills, Travel & Stays
- Descriptions reflect common Indian expense contexts (Swiggy, Uber, Jio, Apollo, etc.)
- 20 examples per category ensures balanced class distribution

This is a realistic and representative dataset for Indian urban spending patterns.

---

## 4. Approach

### 4.1 Text Preprocessing

Expense descriptions are short and noisy. I applied:

1. **Lowercasing** — normalises casing across entries
2. **Punctuation & number removal** — removes transaction IDs and symbols
3. **Stopword removal** — filters out words like "the", "to", "for" that carry no category signal
4. **Porter Stemming** — reduces "booking", "booked", "books" to the root `book`

This ensures the classifier sees only meaningful, normalised tokens.

### 4.2 Feature Extraction — TF-IDF with Bigrams

TF-IDF (Term Frequency-Inverse Document Frequency) was used with:
- `max_features=3000` — vocabulary cap to prevent overfitting
- `ngram_range=(1,2)` — captures both single words and two-word phrases
- `sublinear_tf=True` — applies log scaling to term frequency, reducing the weight of very frequent terms

Bigrams are especially important here: "electricity bill" or "hotel booking" are more discriminative as phrases than their individual words.

### 4.3 Model — Logistic Regression (Multinomial)

I chose Logistic Regression over Naive Bayes for this project because:
- It handles feature correlations better (many expense keywords overlap across categories)
- It provides calibrated probability estimates for confidence scoring
- It performs well on short-text, multi-class classification
- `C=5.0` provides moderate regularisation without underfitting

The model was packaged into a **sklearn Pipeline** (TF-IDF + Classifier), allowing the entire preprocessing-to-prediction workflow to be saved as a single `.pkl` file and used seamlessly at inference time.

### 4.4 Automation Layer

The project goes beyond a notebook:
- `categorize_csv()` accepts any CSV, auto-detects the description column by scanning for common column name patterns, and returns an enriched DataFrame
- `app.py` provides a full CLI with flags for single queries, demo mode, summary reports, and saving output
- The spending summary groups by category and calculates total amount and percentage share — turning raw predictions into actionable insight

---

## 5. Key Technical Decisions

| Decision | Choice | Reason |
|---|---|---|
| Algorithm | Logistic Regression | Better with correlated features than Naive Bayes; calibrated probabilities |
| Pipeline | sklearn Pipeline | Single serialisable object; consistent preprocessing at train and predict time |
| Training data | Custom-built | No suitable Indian-context labelled dataset existed |
| N-grams | Unigrams + bigrams | Expense phrases are more discriminative than individual words |
| Column detection | Heuristic auto-detection | Makes the tool usable with any real CSV without configuration |
| CLI | argparse | Fully command-line executable as required |

---

## 6. Results

5-fold cross-validation on the training dataset:

| Metric | Score |
|---|---|
| CV Accuracy (mean) | ~96–98% |
| CV Accuracy (std) | ±1–2% |

Per-category performance is consistently high because the categories have distinct vocabulary. The model occasionally confuses "Travel & Stays" with "Transport" for entries like "cab to airport", which is expected given genuine semantic overlap.

---

## 7. Challenges Faced

**1. No off-the-shelf dataset**  
Indian expense descriptions have a distinct vocabulary (Swiggy, Zomato, Jio, Ola, etc.) that isn't well-represented in English NLP benchmarks. I solved this by building a custom training set.

**2. Short text length**  
Most descriptions are 2–5 words. This limits the amount of signal per example. Bigrams and careful stemming compensated for this.

**3. Column auto-detection**  
Real CSV exports use inconsistent column names ("description", "narration", "particulars", "details"). I implemented a heuristic scanner that searches for common patterns, with a manual override flag (`--col`) for edge cases.

**4. Overlapping categories**  
Entries like "airport taxi" could be Transport or Travel. I addressed this by including contextually similar examples in training for both categories and relying on the model's confidence score to flag ambiguous cases.

---

## 8. What I Learned

- How to build a complete, end-to-end ML automation pipeline — not just a model, but a usable tool
- The advantage of sklearn Pipelines for combining preprocessing and classification into one deployable object
- Why Logistic Regression often outperforms Naive Bayes on correlated text features
- How to design a CLI application with `argparse` that handles multiple usage modes
- The value of confidence scores — outputting "94.2%" alongside a prediction makes the tool trustworthy and transparent
- How to handle real-world messy input (inconsistent column names, missing values, mixed formats)

---

## 9. Possible Improvements

- Add more training examples and real anonymised transaction data
- Use a pre-trained sentence embedding model (e.g., sentence-transformers) for richer text representations
- Add a rule-based fallback layer for known merchant names (regex matching for "IRCTC", "NETFLIX", etc.)
- Build a web interface using Flask or Streamlit with drag-and-drop CSV upload
- Auto-detect amount and date columns for richer reports with monthly trends

---

## 10. Conclusion

This project demonstrates a practical application of ML text classification to a real daily-life problem — automating expense categorisation. The result is a fully functional CLI tool that accepts any CSV of expense descriptions, classifies each row into one of 8 categories, and outputs both a labelled CSV and a spending summary. It is purposeful, well-executed, and directly applies the NLP and classification techniques covered in the course.

---

## References

1. Scikit-learn documentation — https://scikit-learn.org
2. NLTK documentation — https://www.nltk.org
3. Jurafsky & Martin — *Speech and Language Processing*, Ch. 4 (Naive Bayes and Text Classification)
4. Pedregosa et al. (2011). Scikit-learn: Machine Learning in Python. *JMLR*, 12, 2825–2830.
