import sqlite3
from encryption import decrypt_password
from db_setup import create_database

# Ensure DB table exists
create_database()

# --------------------------
# ADD ENTRY
# --------------------------
def add_entry(website, username, encrypted_password, date_added):
    try:
        conn = sqlite3.connect("password_locker.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO passwords (website, username, password, date_added)
            VALUES (?, ?, ?, ?)
        """, (website, username, encrypted_password, date_added))

        conn.commit()
        conn.close()

    except Exception as e:
        print("Error saving password:", e)

# --------------------------
# GET ALL ENTRIES
# --------------------------
def get_all_entries():
    conn = sqlite3.connect("password_locker.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, website, username, password, date_added FROM passwords")
    rows = cursor.fetchall()
    conn.close()
    return rows

# --------------------------
# DELETE ENTRY
# --------------------------
def delete_entry(entry_id: int):
    try:
        conn = sqlite3.connect("password_locker.db")
        cursor = conn.cursor()

        cursor.execute("DELETE FROM passwords WHERE id = ?", (entry_id,))
        conn.commit()
        conn.close()

    except Exception as e:
        print("Error deleting entry:", e)
