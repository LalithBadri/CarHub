from flask import Flask, render_template, request, redirect, url_for, flash

import db

app = Flask(__name__)
app.secret_key = "dev-secret-key"  # fine for a school project, change before real deployment

CONDITION_LABELS = {1: "Excellent", 2: "Good", 3: "Fair", 4: "Poor"}
CONDITION_FACTORS = {1: 1.05, 2: 1.00, 3: 0.90, 4: 0.75}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/sell", methods=["GET", "POST"])
def sell():
    if request.method == "POST":
        brand = request.form.get("brand", "").strip()
        model = request.form.get("model", "").strip()

        errors = []

        try:
            YOP = int(request.form.get("YOP"))
        except (TypeError, ValueError):
            YOP = None
            errors.append("Please enter a valid year of purchase.")

        try:
            OP = int(request.form.get("OP"))
        except (TypeError, ValueError):
            OP = None
            errors.append("Please enter a valid purchase price.")

        try:
            Dist = int(request.form.get("Dist"))
        except (TypeError, ValueError):
            Dist = None
            errors.append("Please enter a valid distance driven.")

        try:
            cond = int(request.form.get("cond"))
        except (TypeError, ValueError):
            cond = None
        if cond not in CONDITION_FACTORS:
            errors.append("Please choose a condition.")

        if not brand or not model:
            errors.append("Please enter the brand and model.")

        if errors:
            for e in errors:
                flash(e)
            return render_template("sell.html")

        age = 2026 - YOP
        Peryear = age * 0.08 * OP
        Distdip = (Dist / 10000) * 0.015 * OP
        factor = CONDITION_FACTORS[cond]
        val = (OP - Peryear - Distdip) * factor

        db.query(
            """INSERT INTO car_sale_estimates
               (brand, model, purchase_year, purchase_price, mileage_km, condition_grade, estimated_price)
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (brand, model, YOP, OP, Dist, CONDITION_LABELS[cond], round(val, 2)),
            fetch=False,
        )

        breakdown = {
            "age": age,
            "Peryear": round(Peryear, 2),
            "Distdip": round(Distdip, 2),
            "factor": factor,
            "condition_label": CONDITION_LABELS[cond],
        }
        return render_template(
            "sell_result.html", brand=brand, model=model, YOP=YOP, OP=OP,
            val=round(val, 2), breakdown=breakdown
        )

    return render_template("sell.html")


@app.route("/rentals")
def rentals():
    cars = db.query("SELECT * FROM cars WHERE available = TRUE ORDER BY rate_per_day")
    return render_template("rentals.html", cars=cars)


@app.route("/rentals/book/<int:car_id>", methods=["GET", "POST"])
def book_car(car_id):
    car_rows = db.query("SELECT * FROM cars WHERE id = %s", (car_id,))
    if not car_rows:
        flash("That car could not be found.")
        return redirect(url_for("rentals"))
    car = car_rows[0]

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        SD = request.form.get("SD", "").strip()
        RD = request.form.get("RD", "").strip()

        errors = []

        try:
            number = int(request.form.get("number"))
        except (TypeError, ValueError):
            number = None
            errors.append("Please enter a valid phone number.")

        try:
            tot = int(request.form.get("tot"))
        except (TypeError, ValueError):
            tot = None
            errors.append("Please enter a valid number of days.")

        if not name:
            errors.append("Please enter your name.")
        if not SD or not RD:
            errors.append("Please enter both dates.")

        if errors:
            for e in errors:
                flash(e)
            return render_template("book.html", car=car)

        RPD = float(car["rate_per_day"])
        price = RPD * tot

        booking_id = db.query(
            """INSERT INTO rental_bookings
               (car_id, customer_name, customer_phone, start_date, end_date, total_days, total_price)
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (car_id, name, str(number), SD, RD, tot, price),
            fetch=False,
        )

        booking = {"id": booking_id, "name": name, "SD": SD, "RD": RD, "tot": tot, "price": price}
        return render_template("booking_confirmation.html", car=car, booking=booking)

    return render_template("book.html", car=car)


@app.route("/rentals/bookings")
def bookings():
    rows = db.query(
        """SELECT b.*, c.brand, c.model
           FROM rental_bookings b
           JOIN cars c ON c.id = b.car_id
           ORDER BY b.created_at DESC"""
    )
    return render_template("bookings.html", bookings=rows)


if __name__ == "__main__":
    app.run(debug=True)
