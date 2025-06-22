# GitHub Account Switcher

A simple Windows application to switch between multiple GitHub accounts.

## Features

- Add and save multiple GitHub accounts (name and email).
- View the currently configured global Git user.
- Switch the global Git user with a single click.
- Delete saved accounts.

## How to Use

1.  **Run the application**:
    ```bash
    python main.py
    ```

2.  **Add an Account**:
    - Enter the name and email associated with your GitHub account in the "Add New Account" section.
    - Click the "Add Account" button.

3.  **Switch Accounts**:
    - Select an account from the "Saved Accounts" list.
    - Click the "Set as Global" button.

4.  **Delete an Account**:
    - Select an account from the "Saved Accounts" list.
    - Click the "Delete Selected" button.

## Requirements

- Python 3.x
- Git installed and in your system's PATH.

## Files

- `main.py`: The main application script.
- `accounts.json`: Stores the saved GitHub accounts. 