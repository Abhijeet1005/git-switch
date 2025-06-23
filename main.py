# Import the tkinter module for GUI, messagebox for popups, json for file operations, and subprocess for running git commands
import tkinter as tk
from tkinter import messagebox
import json
import subprocess

# The filename where all GitHub account profiles will be stored in JSON format
ACCOUNTS_FILE = "accounts.json"

class AccountSwitcherApp:
    def __init__(self, root):
        """
        Initialize the main application window, load accounts, get the current git user,
        and set up the user interface.
        """
        self.root = root
        self.root.title("GitHub Account Switcher")

        # Load the list of saved accounts from the accounts file
        self.accounts = self.load_accounts()
        # Get the currently configured global git user and email
        self.current_user, self.current_email = self.get_current_git_user()

        # Build the graphical user interface
        self.setup_ui()

    def load_accounts(self):
        """
        Load the list of saved accounts from the accounts JSON file.
        Returns an empty list if the file does not exist or is invalid.
        """
        try:
            with open(ACCOUNTS_FILE, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # If the file doesn't exist or is corrupted, return an empty list
            return []

    def save_accounts(self):
        """
        Save the current list of accounts to the accounts JSON file.
        """
        with open(ACCOUNTS_FILE, "w") as f:
            json.dump(self.accounts, f, indent=4)
    
    def get_current_git_user(self):
        """
        Retrieve the current global git user.name and user.email from git config.
        Returns ("N/A", "N/A") if git is not installed or not configured.
        """
        try:
            # Run git config commands to get the current global user name and email
            user = subprocess.check_output(["git", "config", "--global", "user.name"]).strip().decode()
            email = subprocess.check_output(["git", "config", "--global", "user.email"]).strip().decode()
            return user, email
        except (subprocess.CalledProcessError, FileNotFoundError):
            # If git is not installed or not configured, return placeholders
            return "N/A", "N/A"

    def setup_ui(self):
        """
        Set up all the graphical user interface components, including labels, listboxes,
        entry fields, and buttons for all user actions.
        """
        # Display the currently active global git user at the top
        tk.Label(self.root, text="Current Git User:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.current_user_label = tk.Label(
            self.root,
            text=f"{self.current_user} <{self.current_email}>",
            font=("Helvetica", 10, "bold")
        )
        self.current_user_label.grid(row=0, column=1, columnspan=2, sticky="w", padx=5, pady=5)

        # Section for displaying all saved accounts
        tk.Label(self.root, text="Saved Accounts:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.accounts_listbox = tk.Listbox(self.root, height=5)
        self.accounts_listbox.grid(row=2, column=0, columnspan=3, sticky="we", padx=5, pady=5)
        self.populate_accounts_list()

        # Section for adding a new account (name and email fields)
        tk.Label(self.root, text="Add New Account:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        tk.Label(self.root, text="Name:").grid(row=4, column=0, sticky="w", padx=5)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=4, column=1, sticky="we", padx=5)
        tk.Label(self.root, text="Email:").grid(row=5, column=0, sticky="w", padx=5)
        self.email_entry = tk.Entry(self.root)
        self.email_entry.grid(row=5, column=1, sticky="we", padx=5)
        add_button = tk.Button(self.root, text="Add Account", command=self.add_account)
        add_button.grid(row=5, column=2, padx=5)

        # Buttons for setting the selected account as global and deleting an account
        set_button = tk.Button(self.root, text="Set as Global", command=self.set_global_account)
        set_button.grid(row=6, column=0, pady=10)
        delete_button = tk.Button(self.root, text="Delete Selected", command=self.delete_account)
        delete_button.grid(row=6, column=1, pady=10)

    def populate_accounts_list(self):
        """
        Populate the listbox widget with all saved accounts in the format 'Name <Email>'.
        """
        self.accounts_listbox.delete(0, tk.END)  # Clear the listbox first
        for acc in self.accounts:
            self.accounts_listbox.insert(tk.END, f"{acc['name']} <{acc['email']}>")

    def add_account(self):
        """
        Add a new account to the saved accounts list using the values from the entry fields.
        Prevents adding duplicate emails and empty fields.
        """
        name = self.name_entry.get()
        email = self.email_entry.get()
        if name and email:
            # Check for duplicate email addresses
            if any(acc['email'] == email for acc in self.accounts):
                messagebox.showerror("Error", "Account with this email already exists.")
                return
            # Add the new account to the list and update the file and UI
            self.accounts.append({"name": name, "email": email})
            self.save_accounts()
            self.populate_accounts_list()
            self.name_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
        else:
            # Show an error if either field is empty
            messagebox.showerror("Error", "Name and Email cannot be empty.")

    def set_global_account(self):
        """
        Set the selected account from the listbox as the global git user.name and user.email.
        Updates the display and shows a success or error message.
        """
        selected_index = self.accounts_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select an account to set.")
            return

        account = self.accounts[selected_index[0]]
        try:
            # Use git config to set the global user name and email
            subprocess.run(["git", "config", "--global", "user.name", account['name']], check=True)
            subprocess.run(["git", "config", "--global", "user.email", account['email']], check=True)
            # Refresh the current user display to reflect the change
            self.current_user, self.current_email = self.get_current_git_user()
            self.current_user_label.config(text=f"{self.current_user} <{self.current_email}>")
            messagebox.showinfo("Success", "Global Git account updated successfully.")
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            # Show an error if git is not available or the command fails
            messagebox.showerror("Error", f"Failed to set Git config: {e}")

    def delete_account(self):
        """
        Delete the selected account from the saved accounts list after confirmation.
        Updates the file and the UI accordingly.
        """
        selected_index = self.accounts_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select an account to delete.")
            return
        # Ask the user to confirm deletion
        if messagebox.askyesno("Confirm", "Are you sure you want to delete the selected account?"):
            self.accounts.pop(selected_index[0])
            self.save_accounts()
            self.populate_accounts_list()

# Main entry point for the application

def main():
    """
    Create the main Tkinter window and start the AccountSwitcherApp.
    """
    root = tk.Tk()
    app = AccountSwitcherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 