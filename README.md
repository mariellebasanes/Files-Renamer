# Rename File Application (Flask)

A small Flask app that lists a folder and renames files, with **old name** and **new name** shown side by side.

## Run

1. Install dependencies (use `python -m pip` if `pip` doesn't work):
   ```bash
   python -m pip install -r requirements.txt
   ```
2. Start the app:
   ```bash
   python app.py
   ```
3. Open **http://127.0.0.1:5000** in your browser.

## Usage

- **Load Folder**: Leave the path blank to use the app folder, or enter a folder path and click **Load Folder**.
- The table shows **Old name** (current filename) and **New name** (editable). Edit the new name and click **Rename** on that row to rename the file.

Files and folders are listed; renaming applies to both. The app only allows renaming inside the project folder for safety.
