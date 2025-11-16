#!/usr/bin/env python3
"""
main.py
Console menu for the Password Locker project (Day 5).
Fully compatible with encryption.py and password_manager.py
"""

from datetime import datetime
import sys
import getpass

# Import modules
try:
    from encryption import encrypt_password, decrypt_password, ensure_key
    from password_manager import add_entry, get_all_entries, delete_entry
except Exception as e:
    print("Error importing project modules:", e)
    sys.exit(1)

# Load encryption key
key = ensure_key()


# ---------------------------------------------------
# ADD ENTRY
# ---------------------------------------------------
def prompt_add_entry():
    print("\n--- Add New Password ---")
    website = input("Website / Service: ").strip()
    username = input("Username / Email: ").strip()
    password = getpass.getpass("Password (hidden): ").strip()

    if not website or not username or not password:
        print("❌ All fields are required.")
        return

    try:
        encrypted = encrypt_password(password, key)
    except Exception as e:
        print("Encryption failed:", e)
        return

    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        add_entry(website, username, encrypted, date_str)
        print("✅ Password saved successfully!")
    except Exception as e:
        print("Error saving to database:", e)


# ---------------------------------------------------
# DISPLAY ENTRIES
# ---------------------------------------------------
def display_entries():
    print("\n--- Saved Passwords ---")
    try:
        rows = get_all_entries()
    except Exception as e:
        print("Error fetching entries:", e)
        return

    if not rows:
        print("⚠️ No passwords saved yet.")
        return

    header = f"{'ID':<4} {'Website':<25} {'Username':<25} {'Password':<20} {'Date'}"
    print(header)
    print("-" * len(header))

    for row in rows:
        try:
            row_id = row[0]
            website = str(row[1])[:25]
            username = str(row[2])[:25]
            encrypted_password = row[3]
            date_str = str(row[4])

            try:
                decrypted = decrypt_password(encrypted_password, key)
            except:
                decrypted = "<error>"

            print(f"{row_id:<4} {website:<25} {username:<25} {decrypted:<20} {date_str}")
        except Exception as e:
            print("Row read error:", e)


# ---------------------------------------------------
# DELETE PASSWORD BY ID
# ---------------------------------------------------
def delete_password():
    print("\n--- Delete Password ---")
    entry_id = input("Enter ID to delete: ").strip()

    if not entry_id.isdigit():
        print("❌ Invalid ID. Enter a number.")
        return

    try:
        delete_entry(int(entry_id))
        print("🗑️ Entry deleted successfully!")
    except Exception as e:
        print("Error deleting entry:", e)


# ---------------------------------------------------
# MENU LOOP
# ---------------------------------------------------
def menu_loop():
    while True:
        print("\n=== Password Locker ===")
        print("1. Add new password")
        print("2. View saved passwords")
        print("3. Delete password")
        print("4. Exit")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            prompt_add_entry()
        elif choice == "2":
            display_entries()
        elif choice == "3":
            delete_password()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("❌ Invalid choice — enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    menu_loop()
