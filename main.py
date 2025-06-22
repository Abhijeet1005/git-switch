import tkinter as tk
from tkinter import messagebox
import json
import subprocess

ACCOUNTS_FILE = "accounts.json"

class AccountSwitcherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub Account Switcher")

        self.accounts = self.load_accounts()
        self.current_user, self.current_email = self.get_current_git_user()

        self.setup_ui()

    def load_accounts(self):
        try:
            with open(ACCOUNTS_FILE, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_accounts(self):
        with open(ACCOUNTS_FILE, "w") as f:
            json.dump(self.accounts, f, indent=4)

def main():
    root = tk.Tk()
    app = AccountSwitcherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 