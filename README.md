# CarHub
**ALL HTML FRONT END PROGRAMMING IS DONE BY AI, LOGIC AND BACK-END PYTHON AND MYSQL PROGRAMMING IS DONE BY MYSELF**
A small Python + MySQL website for two things:

1. **Renting a car** — browse a fleet, book one, and see a total price.
2. **Selling a car** — enter your car's details and get an estimated resale price, with the working shown.

## How the resale price is estimated

```
age      = 2026 - year_of_purchase
Peryear  = age * 0.08 * purchase_price      (8% of price, per year)
Distdip  = (distance_km / 10000) * 0.015 * purchase_price
factor   = 1.05 / 1.00 / 0.90 / 0.75         (Excellent / Good / Fair / Poor)
value    = (purchase_price - Peryear - Distdip) * factor
```

See [`app.py`](app.py)'s `sell()` route for the exact implementation.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create the database:
   ```bash
   mysql -u root -p < database/schema.sql
   ```
3. Copy `.env.example` to `.env` and fill in your MySQL credentials (never commit `.env` — it's already in `.gitignore`):
   ```bash
   cp .env.example .env
   ```
4. Run the website:
   ```bash
   python app.py
   ```
5. Open `http://127.0.0.1:5000` in your browser.

## Project structure

```
carhub/
├── app.py                 # Flask routes + the resale-price formula
├── db.py                    # MySQL connection helper
├── database/schema.sql        # Tables + sample rental fleet
├── templates/                  # HTML pages, with CSS/JS inline (no separate static files)
├── requirements.txt
├── .env.example
└── .gitignore
```
