from flask import Flask, render_template, request, redirect, session
from encryption import ensure_key, encrypt_password, decrypt_password
from password_manager import add_entry, get_all_entries, delete_entry, get_entry_by_id, update_entry
from password_generator import generate_password
from datetime import datetime
import bcrypt
import os

app = Flask(__name__)
app.secret_key = "supersecret_flask_key"

# Load encryption key
key = ensure_key()

# Load stored master password hash
MASTER_HASH = open("master.key", "rb").read()


# LOGIN REQUIRED DECORATOR — only for viewing dashboard
def login_required(func):
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return redirect("/login")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


# MASTER LOGIN PAGE
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        entered = request.form["password"].encode()

        if bcrypt.checkpw(entered, MASTER_HASH):
            session["user"] = "authenticated"
            return redirect("/")
        else:
            return render_template("login.html", error="Invalid Master Password")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# DASHBOARD — requires master key
@app.route("/")
@login_required
def home():
    rows = get_all_entries()
    decrypted_rows = []

    for r in rows:
        decrypted_pw = decrypt_password(r[3], key)
        decrypted_rows.append((r[0], r[1], r[2], decrypted_pw, r[4]))

    return render_template("index.html", rows=decrypted_rows)


# ADD PASSWORD — DOES NOT REQUIRE MASTER LOGIN
@app.route("/add", methods=["POST"])
def add_password():
    website = request.form["website"]
    username = request.form["username"]

    password = generate_password()
    encrypted = encrypt_password(password, key)
    date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    add_entry(website, username, encrypted, date_added)
    return redirect("/login")   # redirect to login page


# DELETE PASSWORD — protected
@app.route("/delete/<int:id>")
@login_required
def delete_password(id):
    delete_entry(id)
    return redirect("/")


# EDIT PAGE — protected
@app.route("/edit/<int:id>")
@login_required
def edit_page(id):
    row = get_entry_by_id(id)
    decrypted_pw = decrypt_password(row[3], key)
    return render_template("edit.html", row=row, password=decrypted_pw)


# UPDATE PASSWORD — protected
@app.route("/update/<int:id>", methods=["POST"])
@login_required
def update_password(id):
    website = request.form["website"]
    username = request.form["username"]
    password = request.form["password"]

    encrypted = encrypt_password(password, key)
    update_entry(id, website, username, encrypted)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
