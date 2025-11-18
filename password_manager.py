import sqlite3
from db_setup import create_database

create_database()

def add_entry(website, username, encrypted_password, date_added):
    try:
        conn = sqlite3.connect("password_locker.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO passwords (website, username, password, date_added)
            VALUES (?, ?, ?, ?)
        """, (website, username, encrypted_password, date_added))
        conn.commit()
    except Exception as e:
        print("Error saving password:", e)
    finally:
        conn.close()

def get_all_entries():
    conn = sqlite3.connect("password_locker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, website, username, password, date_added FROM passwords")
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_entry(entry_id: int):
    try:
        conn = sqlite3.connect("password_locker.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM passwords WHERE id = ?", (entry_id,))
        conn.commit()
    except Exception as e:
        print("Error deleting entry:", e)
    finally:
        conn.close()
