"""
generate_data.py - Generates training data and a sample expenses CSV.
Run this once to create the data/ folder contents.
Usage: python generate_data.py
"""

import os
import csv
import random

os.makedirs('data', exist_ok=True)

# ── Training Data ─────────────────────────────────────────────────────────────
# Each entry: (description, category)

TRAINING_DATA = [
    # Food & Dining
    ("Swiggy order", "Food & Dining"),
    ("Zomato delivery", "Food & Dining"),
    ("McDonald's", "Food & Dining"),
    ("Dominos pizza", "Food & Dining"),
    ("KFC bucket meal", "Food & Dining"),
    ("Subway sandwich", "Food & Dining"),
    ("Restaurant dinner", "Food & Dining"),
    ("Cafe coffee", "Food & Dining"),
    ("Starbucks latte", "Food & Dining"),
    ("Lunch at canteen", "Food & Dining"),
    ("Grocery store", "Food & Dining"),
    ("BigBasket order", "Food & Dining"),
    ("Blinkit groceries", "Food & Dining"),
    ("Milk and bread", "Food & Dining"),
    ("Street food", "Food & Dining"),
    ("Pizza hut order", "Food & Dining"),
    ("Burger King meal", "Food & Dining"),
    ("Ice cream parlour", "Food & Dining"),
    ("Juice bar", "Food & Dining"),
    ("Bakery items", "Food & Dining"),

    # Transport
    ("Uber ride", "Transport"),
    ("Ola cab", "Transport"),
    ("Rapido bike", "Transport"),
    ("Auto rickshaw", "Transport"),
    ("Bus ticket", "Transport"),
    ("Metro card recharge", "Transport"),
    ("Petrol pump", "Transport"),
    ("Fuel refill", "Transport"),
    ("Train ticket", "Transport"),
    ("Flight booking", "Transport"),
    ("Taxi fare", "Transport"),
    ("Parking fee", "Transport"),
    ("Toll charge", "Transport"),
    ("InDrive trip", "Transport"),
    ("BluSmart cab", "Transport"),
    ("BMTC bus pass", "Transport"),
    ("IRCTC train", "Transport"),
    ("SpiceJet flight", "Transport"),
    ("IndiGo ticket", "Transport"),
    ("Cab to airport", "Transport"),

    # Shopping
    ("Amazon order", "Shopping"),
    ("Flipkart purchase", "Shopping"),
    ("Myntra clothes", "Shopping"),
    ("Ajio outfit", "Shopping"),
    ("Meesho order", "Shopping"),
    ("Nykaa cosmetics", "Shopping"),
    ("Shoes purchase", "Shopping"),
    ("T-shirt buy", "Shopping"),
    ("Jeans from mall", "Shopping"),
    ("Electronics store", "Shopping"),
    ("Book purchase", "Shopping"),
    ("Stationary shop", "Shopping"),
    ("Home decor item", "Shopping"),
    ("Croma gadget", "Shopping"),
    ("Reliance Digital", "Shopping"),
    ("Snitch clothing", "Shopping"),
    ("Westside apparel", "Shopping"),
    ("H&M purchase", "Shopping"),
    ("Zara outfit", "Shopping"),
    ("Furniture order", "Shopping"),

    # Entertainment
    ("Netflix subscription", "Entertainment"),
    ("Hotstar premium", "Entertainment"),
    ("Amazon Prime", "Entertainment"),
    ("Spotify music", "Entertainment"),
    ("Movie tickets", "Entertainment"),
    ("BookMyShow", "Entertainment"),
    ("PVR cinemas", "Entertainment"),
    ("Gaming top-up", "Entertainment"),
    ("Steam game", "Entertainment"),
    ("YouTube Premium", "Entertainment"),
    ("Disney+ Hotstar", "Entertainment"),
    ("SonyLIV subscription", "Entertainment"),
    ("Zee5 plan", "Entertainment"),
    ("Concert tickets", "Entertainment"),
    ("Amusement park", "Entertainment"),
    ("PS5 game", "Entertainment"),
    ("PUBG UC purchase", "Entertainment"),
    ("Ludo tournament", "Entertainment"),
    ("Chess app premium", "Entertainment"),
    ("Theme park entry", "Entertainment"),

    # Health
    ("Pharmacy medicine", "Health"),
    ("Apollo pharmacy", "Health"),
    ("Doctor consultation", "Health"),
    ("Hospital bill", "Health"),
    ("MedPlus store", "Health"),
    ("1mg order", "Health"),
    ("Practo appointment", "Health"),
    ("Gym membership", "Health"),
    ("Cult.fit session", "Health"),
    ("Yoga class", "Health"),
    ("Fitness tracker", "Health"),
    ("Eye checkup", "Health"),
    ("Dental clinic", "Health"),
    ("Blood test", "Health"),
    ("Health insurance", "Health"),
    ("Vitamins supplement", "Health"),
    ("Protein powder", "Health"),
    ("Physio session", "Health"),
    ("Lab test fee", "Health"),
    ("Ambulance charge", "Health"),

    # Education
    ("Udemy course", "Education"),
    ("Coursera subscription", "Education"),
    ("College fee", "Education"),
    ("Tuition payment", "Education"),
    ("Exam registration", "Education"),
    ("Books for class", "Education"),
    ("LinkedIn Learning", "Education"),
    ("NPTEL certificate", "Education"),
    ("Coding bootcamp", "Education"),
    ("Skill India course", "Education"),
    ("Online tutorial", "Education"),
    ("Test series fee", "Education"),
    ("Library membership", "Education"),
    ("Study material", "Education"),
    ("Workshop fee", "Education"),
    ("edX course", "Education"),
    ("Internshala course", "Education"),
    ("Unacademy plan", "Education"),
    ("BYJU'S subscription", "Education"),
    ("Khan Academy donate", "Education"),

    # Utilities & Bills
    ("Electricity bill", "Utilities & Bills"),
    ("Water bill", "Utilities & Bills"),
    ("Internet recharge", "Utilities & Bills"),
    ("Jio recharge", "Utilities & Bills"),
    ("Airtel plan", "Utilities & Bills"),
    ("BSNL bill", "Utilities & Bills"),
    ("Gas cylinder", "Utilities & Bills"),
    ("DTH recharge", "Utilities & Bills"),
    ("Tata Sky renewal", "Utilities & Bills"),
    ("Mobile bill", "Utilities & Bills"),
    ("Broadband bill", "Utilities & Bills"),
    ("LPG booking", "Utilities & Bills"),
    ("Postpaid bill", "Utilities & Bills"),
    ("OTT bundle bill", "Utilities & Bills"),
    ("Cable TV bill", "Utilities & Bills"),
    ("Vi recharge", "Utilities & Bills"),
    ("MSEB electricity", "Utilities & Bills"),
    ("Society maintenance", "Utilities & Bills"),
    ("Property tax", "Utilities & Bills"),
    ("Water tanker", "Utilities & Bills"),

    # Travel & Stays
    ("Hotel booking", "Travel & Stays"),
    ("MakeMyTrip hotel", "Travel & Stays"),
    ("OYO room", "Travel & Stays"),
    ("Airbnb stay", "Travel & Stays"),
    ("Goibibo trip", "Travel & Stays"),
    ("Holiday package", "Travel & Stays"),
    ("Hostel stay", "Travel & Stays"),
    ("Resort booking", "Travel & Stays"),
    ("Trip expenses", "Travel & Stays"),
    ("Sightseeing tour", "Travel & Stays"),
    ("Treebo hotel", "Travel & Stays"),
    ("FabHotels stay", "Travel & Stays"),
    ("Visa fee", "Travel & Stays"),
    ("Travel insurance", "Travel & Stays"),
    ("Yatra booking", "Travel & Stays"),
    ("EaseMyTrip flight", "Travel & Stays"),
    ("Weekend getaway", "Travel & Stays"),
    ("Camping gear rent", "Travel & Stays"),
    ("Museum entry", "Travel & Stays"),
    ("Tour guide fee", "Travel & Stays"),
]

# ── Save training CSV ─────────────────────────────────────────────────────────

train_path = os.path.join('data', 'training_data.csv')
with open(train_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['description', 'category'])
    writer.writerows(TRAINING_DATA)

print(f"Training data saved → {train_path}  ({len(TRAINING_DATA)} rows)")

# ── Generate sample expenses CSV ──────────────────────────────────────────────

random.seed(42)

sample_expenses = [
    ("2026-03-01", "Swiggy biryani order", 280),
    ("2026-03-01", "Uber ride to college", 95),
    ("2026-03-02", "Amazon headphones", 1299),
    ("2026-03-02", "Netflix monthly plan", 499),
    ("2026-03-03", "Pharmacy paracetamol", 45),
    ("2026-03-03", "Jio prepaid recharge", 239),
    ("2026-03-04", "Dominos pizza night", 450),
    ("2026-03-04", "BookMyShow movie", 320),
    ("2026-03-05", "Udemy Python course", 399),
    ("2026-03-05", "Petrol refill", 500),
    ("2026-03-06", "Zomato lunch delivery", 180),
    ("2026-03-06", "OYO room weekend", 1200),
    ("2026-03-07", "Myntra shirt purchase", 799),
    ("2026-03-07", "Gym monthly fee", 600),
    ("2026-03-08", "BigBasket groceries", 1100),
    ("2026-03-08", "Metro card top-up", 200),
    ("2026-03-09", "Electricity bill pay", 850),
    ("2026-03-09", "Starbucks coffee", 350),
    ("2026-03-10", "Flipkart earbuds", 999),
    ("2026-03-10", "Doctor visit fee", 300),
    ("2026-03-11", "Rapido bike ride", 55),
    ("2026-03-11", "Coursera certificate", 2999),
    ("2026-03-12", "KFC family bucket", 700),
    ("2026-03-12", "Spotify premium", 119),
    ("2026-03-13", "Bus pass renewal", 150),
    ("2026-03-13", "1mg medicine order", 220),
    ("2026-03-14", "MakeMyTrip hotel", 3500),
    ("2026-03-14", "Airtel postpaid bill", 399),
    ("2026-03-15", "Nykaa skincare", 650),
    ("2026-03-15", "Zara outfit mall", 2200),
]

sample_path = os.path.join('data', 'my_expenses.csv')
with open(sample_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['date', 'description', 'amount'])
    writer.writerows(sample_expenses)

print(f"Sample expenses saved → {sample_path}  ({len(sample_expenses)} rows)")
print("\nNow run:  python train.py")
