from flask import Flask, render_template, request, redirect
from encryption import ensure_key, encrypt_password, decrypt_password
from password_manager import add_entry, get_all_entries, delete_entry
from datetime import datetime

app = Flask(__name__)
key = ensure_key()

@app.route("/")
def home():
    rows = get_all_entries()

    # Decrypt passwords for display
    decrypted_rows = []
    for r in rows:
        decrypted_pw = decrypt_password(r[3], key)
        decrypted_rows.append((r[0], r[1], r[2], decrypted_pw, r[4]))

    return render_template("index.html", rows=decrypted_rows)

@app.route("/add", methods=["POST"])
def add_password():
    website = request.form["website"]
    username = request.form["username"]
    password = request.form["password"]

    encrypted = encrypt_password(password, key)
    date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    add_entry(website, username, encrypted, date_added)

    return redirect("/")

@app.route("/delete/<int:id>")
def delete_password_route(id):
    delete_entry(id)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
