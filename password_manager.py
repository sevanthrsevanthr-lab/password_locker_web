import sqlite3
from encryption import ensure_key, encrypt_password, decrypt_password
from db_setup import create_database
from datetime import datetime

# Make sure table exists
create_database()

# Load or create encryption key
key = ensure_key()


# ---------------------------------------------------
# ADD ENTRY
# Called by main.py with encrypted password (bytes)
# ---------------------------------------------------
def add_entry(website, username, encrypted_password, date):
    try:
        conn = sqlite3.connect("password_locker.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO passwords (website, username, password, date) VALUES (?, ?, ?, ?)",
            (website, username, encrypted_password, date)
        )
        conn.commit()
        conn.close()

        print("✅ Password saved securely!")

    except Exception as e:
        print("Error saving password:", e)


# ---------------------------------------------------
# GET ALL ENTRIES
# Main.py expects: id, website, username, password, date
# ---------------------------------------------------
def get_all_entries():
    conn = sqlite3.connect("password_locker.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, website, username, password, date FROM passwords")
    rows = cursor.fetchall()

    conn.close()
    return rows


# ---------------------------------------------------
# DELETE ENTRY (NEW)
# Removes a password by ID
# ---------------------------------------------------
def delete_entry(entry_id: int):
    try:
        conn = sqlite3.connect("password_locker.db")
        cursor = conn.cursor()

        cursor.execute("DELETE FROM passwords WHERE id = ?", (entry_id,))
        conn.commit()
        conn.close()

        print("🗑️ Entry deleted successfully!")

    except Exception as e:
        print("Error deleting entry:", e)


# ---------------------------------------------------
# OPTIONAL: VIEW passwords (only if running this file directly)
# ---------------------------------------------------
def view_passwords():
    try:
        conn = sqlite3.connect("password_locker.db")
        cursor = conn.cursor()

        cursor.execute("SELECT website, username, password FROM passwords")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            print("⚠️ No passwords found.")
            return

        print("\nSaved Passwords:")
        for website, username, encrypted_password in rows:
            decrypted = decrypt_password(encrypted_password, key)
            print(f"🌐 Website: {website} | 👤 Username: {username} | 🔐 Password: {decrypted}")

    except Exception as e:
        print("Failed to fetch entries from DB:", e)


# ---------------------------------------------------
# Standalone menu (not used by main.py)
# ---------------------------------------------------
if __name__ == "__main__":
    while True:
        print("\n1️⃣ Add Password")
        print("2️⃣ View Passwords")
        print("3️⃣ Delete Password by ID")
        print("4️⃣ Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            website = input("Enter website: ").strip()
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()

            encrypted = encrypt_password(password, key)
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            add_entry(website, username, encrypted, date)

        elif choice == "2":
            view_passwords()

        elif choice == "3":
            entry_id = input("Enter ID to delete: ")
            if entry_id.isdigit():
                delete_entry(int(entry_id))
            else:
                print("Invalid ID")

        elif choice == "4":
            print("Exiting...")
            break

        else:
            print("Invalid choice, try again.")
