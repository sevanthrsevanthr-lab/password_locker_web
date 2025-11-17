from datetime import datetime
import sys

from encryption import encrypt_password, decrypt_password, ensure_key
from password_manager import add_entry, get_all_entries, delete_entry
from password_generator import generate_password

key = ensure_key()

def prompt_add_entry():
    print("\n--- Add New Password ---")
    website = input("Website / Service: ").strip()
    username = input("Username / Email: ").strip()

    if not website or not username:
        print("❌ Website and username required.")
        return

    password = generate_password()
    print("Generated Password:", password)

    encrypted = encrypt_password(password, key)
    date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    add_entry(website, username, encrypted, date_added)
    print("✅ Password saved successfully!")

def display_entries():
    print("\n--- Saved Passwords ---")
    rows = get_all_entries()

    if not rows:
        print("⚠️ No passwords found.")
        return

    header = f"{'ID':<4} {'Website':<25} {'Username':<25} {'Password':<20} {'Date'}"
    print(header)
    print("-" * len(header))

    for row in rows:
        row_id, website, username, encrypted, date = row
        try:
            decrypted = decrypt_password(encrypted, key)
        except:
            decrypted = "<error>"
        print(f"{row_id:<4} {website:<25} {username:<25} {decrypted:<20} {date}")

def delete_password():
    entry_id = input("Enter ID to delete: ").strip()
    if entry_id.isdigit():
        delete_entry(int(entry_id))
        print("🗑️ Entry deleted!")
    else:
        print("❌ Invalid ID.")

def menu_loop():
    while True:
        print("\n=== Password Locker ===")
        print("1. Add new password")
        print("2. View saved passwords")
        print("3. Delete password")
        print("4. Exit")

        choice = input("Choose (1-4): ")

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
            print("❌ Invalid choice.")

if __name__ == "__main__":
    menu_loop()
