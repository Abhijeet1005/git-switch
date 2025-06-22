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

def main():
    root = tk.Tk()
    app = AccountSwitcherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 