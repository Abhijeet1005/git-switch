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
    
    def get_current_git_user(self):
        try:
            user = subprocess.check_output(["git", "config", "--global", "user.name"]).strip().decode()
            email = subprocess.check_output(["git", "config", "--global", "user.email"]).strip().decode()
            return user, email
        except (subprocess.CalledProcessError, FileNotFoundError):
            return "N/A", "N/A"

    def setup_ui(self):
        # Current user display
        tk.Label(self.root, text="Current Git User:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.current_user_label = tk.Label(self.root, text=f"{self.current_user} <{self.current_email}>", font=("Helvetica", 10, "bold"))
        self.current_user_label.grid(row=0, column=1, columnspan=2, sticky="w", padx=5, pady=5)

        # Saved accounts
        tk.Label(self.root, text="Saved Accounts:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.accounts_listbox = tk.Listbox(self.root, height=5)
        self.accounts_listbox.grid(row=2, column=0, columnspan=3, sticky="we", padx=5, pady=5)
        self.populate_accounts_list()

        # Add new account
        tk.Label(self.root, text="Add New Account:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        tk.Label(self.root, text="Name:").grid(row=4, column=0, sticky="w", padx=5)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=4, column=1, sticky="we", padx=5)
        tk.Label(self.root, text="Email:").grid(row=5, column=0, sticky="w", padx=5)
        self.email_entry = tk.Entry(self.root)
        self.email_entry.grid(row=5, column=1, sticky="we", padx=5)
        add_button = tk.Button(self.root, text="Add Account", command=self.add_account)
        add_button.grid(row=5, column=2, padx=5)

        # Actions
        set_button = tk.Button(self.root, text="Set as Global", command=self.set_global_account)
        set_button.grid(row=6, column=0, pady=10)
        delete_button = tk.Button(self.root, text="Delete Selected", command=self.delete_account)
        delete_button.grid(row=6, column=1, pady=10)


    def populate_accounts_list(self):
        self.accounts_listbox.delete(0, tk.END)
        for acc in self.accounts:
            self.accounts_listbox.insert(tk.END, f"{acc['name']} <{acc['email']}>")

    def add_account(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        if name and email:
            if any(acc['email'] == email for acc in self.accounts):
                messagebox.showerror("Error", "Account with this email already exists.")
                return

            self.accounts.append({"name": name, "email": email})
            self.save_accounts()
            self.populate_accounts_list()
            self.name_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Name and Email cannot be empty.")

    def set_global_account(self):
        selected_index = self.accounts_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select an account to set.")
            return

        account = self.accounts[selected_index[0]]
        try:
            subprocess.run(["git", "config", "--global", "user.name", account['name']], check=True)
            subprocess.run(["git", "config", "--global", "user.email", account['email']], check=True)
            self.current_user, self.current_email = self.get_current_git_user()
            self.current_user_label.config(text=f"{self.current_user} <{self.current_email}>")
            messagebox.showinfo("Success", "Global Git account updated successfully.")
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            messagebox.showerror("Error", f"Failed to set Git config: {e}")

    def delete_account(self):
        selected_index = self.accounts_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select an account to delete.")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete the selected account?"):
            self.accounts.pop(selected_index[0])
            self.save_accounts()
            self.populate_accounts_list()

def main():
    root = tk.Tk()
    app = AccountSwitcherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 