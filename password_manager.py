import sqlite3
from db_setup import create_database

create_database()


def add_entry(website, username, encrypted_password, date_added):
    conn = sqlite3.connect("password_locker.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO passwords (website, username, password, date_added)
        VALUES (?, ?, ?, ?)
    """, (website, username, encrypted_password, date_added))
    conn.commit()
    conn.close()


def get_all_entries():
    conn = sqlite3.connect("password_locker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, website, username, password, date_added FROM passwords")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_entry_by_id(entry_id):
    conn = sqlite3.connect("password_locker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM passwords WHERE id = ?", (entry_id,))
    row = cursor.fetchone()
    conn.close()
    return row


def update_entry(entry_id, website, username, encrypted_password):
    conn = sqlite3.connect("password_locker.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE passwords
        SET website=?, username=?, password=?
        WHERE id=?
    """, (website, username, encrypted_password, entry_id))
    conn.commit()
    conn.close()


def delete_entry(entry_id):
    conn = sqlite3.connect("password_locker.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM passwords WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()
