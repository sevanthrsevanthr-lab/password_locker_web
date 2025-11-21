from flask import Flask, render_template, request, redirect, session, jsonify
from encryption import ensure_key, encrypt_password, decrypt_password
from password_manager import (
    add_entry, get_all_entries, delete_entry,
    get_entry_by_id, update_entry, get_entry_by_username
)
from password_generator import generate_password
from datetime import datetime
import bcrypt

app = Flask(__name__)
app.secret_key = "supersecret_flask_key"

# Load encryption key
key = ensure_key()

# Load master password hash
MASTER_HASH = open("master.key", "rb").read()


# =====================================================================
#  LOGIN REQUIRED DECORATOR
# =====================================================================
def login_required(func):
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return redirect("/login")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


# =====================================================================
#  MASTER LOGIN PAGE
# =====================================================================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        entered_pw = request.form["password"].encode()

        if bcrypt.checkpw(entered_pw, MASTER_HASH):
            session["user"] = "authenticated"
            return redirect("/")
        else:
            return render_template("login.html", error="Invalid Master Password")

    return render_template("login.html")


# =====================================================================
#  LOGOUT
# =====================================================================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# =====================================================================
#  MAIN PASSWORD VAULT DASHBOARD
# =====================================================================
@app.route("/")
@login_required
def home():
    rows = get_all_entries()
    decrypted_rows = []

    for r in rows:
        decrypted_pw = decrypt_password(r[3], key)
        decrypted_rows.append((r[0], r[1], r[2], decrypted_pw, r[4]))

    return render_template("index.html", rows=decrypted_rows)


# =====================================================================
#  ADD PASSWORD → Then go to DEMO LOGIN
# =====================================================================
@app.route("/add", methods=["POST"])
def add_password():
    website = request.form["website"]
    username = request.form["username"]

    password = generate_password()
    encrypted = encrypt_password(password, key)
    date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    add_entry(website, username, encrypted, date_added)

    return redirect("/demo-login")


# =====================================================================
#  DEMO LOGIN PAGE
# =====================================================================
@app.route("/demo-login", methods=["GET", "POST"])
def demo_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        row = get_entry_by_username(username)

        if not row:
            return render_template("demo_login.html", error="❌ User not found")

        stored_pw = decrypt_password(row[3], key)

        if password == stored_pw:
            return render_template(
                "demo_login.html",
                success="✔ Login Successful!",
                logged_user=username
            )
        else:
            return render_template("demo_login.html", error="❌ Incorrect Password")

    return render_template("demo_login.html")


# =====================================================================
#  ⭐ API FOR PASSWORD AUTO-FILL (Used by JS)
# =====================================================================
@app.route("/get-password", methods=["POST"])
def get_password_api():
    username = request.form["username"]
    row = get_entry_by_username(username)

    if row:
        decrypted = decrypt_password(row[3], key)
        return jsonify({"password": decrypted})

    return jsonify({"password": ""})


# =====================================================================
#  DEMO DASHBOARD
# =====================================================================
@app.route("/demo-dashboard")
def demo_dashboard():
    return render_template("demo_dashboard.html")


# =====================================================================
#  DELETE ENTRY
# =====================================================================
@app.route("/delete/<int:id>")
@login_required
def delete_password(id):
    delete_entry(id)
    return redirect("/")


# =====================================================================
#  EDIT PAGE
# =====================================================================
@app.route("/edit/<int:id>")
@login_required
def edit_page(id):
    row = get_entry_by_id(id)
    decrypted = decrypt_password(row[3], key)
    return render_template("edit.html", row=row, password=decrypted)


# =====================================================================
#  UPDATE ENTRY
# =====================================================================
@app.route("/update/<int:id>", methods=["POST"])
@login_required
def update_password(id):
    website = request.form["website"]
    username = request.form["username"]
    password = request.form["password"]

    encrypted = encrypt_password(password, key)
    update_entry(id, website, username, encrypted)

    return redirect("/")


# =====================================================================
#  RUN APP
# =====================================================================
if __name__ == "__main__":
    app.run(debug=True)
