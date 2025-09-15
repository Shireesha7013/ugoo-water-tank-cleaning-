from flask import Flask, render_template, request, redirect, url_for, session
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret123"  # Required for session

# File where bookings are stored
BOOKINGS_FILE = os.path.join(os.path.dirname(__file__), "bookings.txt")

# Dummy admin login
ADMIN_USER = "admin"
ADMIN_PASS = "password"

# ---------------- Ensure bookings.txt exists ----------------
def ensure_file():
    if not os.path.exists(BOOKINGS_FILE):
        with open(BOOKINGS_FILE, "w") as f:
            f.write("Bookings:\n")

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------------- CUSTOMER FORM ----------------
@app.route("/form", methods=["GET"])
def form():
    return render_template("form.html")

@app.route("/bookings", methods=["POST"])
def save_booking():
    name = request.form.get("name")
    phone = request.form.get("phone")
    service = request.form.get("service")
    address = request.form.get("address")  # Removed extra comma
    date = request.form.get("date")
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ensure_file()
    with open(BOOKINGS_FILE, "a") as f:
        f.write(f"{time} | {name} | {phone} | {service} | {address} | {date}\n")  # Ensure proper string formatting

    return render_template("success.html", name=name, service=service, date=date, address=address)

# ---------------- ADMIN LOGIN ----------------
@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    ensure_file()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Simple login check
        if username == "admin" and password == "1234":
            bookings = []
            with open(BOOKINGS_FILE, "r") as f:
                lines = f.readlines()[1:]  # skip "Bookings:" line
                for line in lines:
                    parts = line.strip().split(" | ")
                    if len(parts) == 6:  # 6 fields: time, name, phone, service, address, date
                        bookings.append({
                            "time": parts[0],
                            "name": parts[1],
                            "phone": parts[2],
                            "service": parts[3],
                            "address": parts[4],
                            "date": parts[5]
                        })
            return render_template("admin.html", bookings=bookings)
        else:
            return render_template("admin_login.html", error="Invalid credentials!")

    return render_template("admin_login.html")

# ---------------- ADMIN BOOKINGS VIEW ----------------
@app.route("/show_bookings", methods=["GET"])
def show_bookings():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    ensure_file()
    bookings = []
    with open(BOOKINGS_FILE, "r") as f:
        lines = f.readlines()[1:]  # Skip header
        for line in lines:
            parts = line.strip().split(" | ")
            if len(parts) == 6:  # 6 fields: time, name, phone, service, address, date
                bookings.append({
                    "time": parts[0],
                    "name": parts[1],
                    "phone": parts[2],
                    "service": parts[3],
                    "address":parts[4],
                    "date": parts[5]
                })
    return render_template("bookings.html", bookings=bookings)

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("admin_login"))

# ---------------- SERVICE DETAIL ROUTES ----------------
@app.route("/detailed1")
def detailed1():
    return render_template("detailed1.html")

@app.route("/detailed2")
def detailed2():
    return render_template("detailed2.html")

@app.route("/detailed3")
def detailed3():
    return render_template("detailed3.html")

if __name__ == "__main__":
    app.run(debug=True)