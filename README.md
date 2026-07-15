# Gangotri Firestone LLP — Hexochems Website

![CI](https://github.com/unknown-umt-07/Gangotri-firestone-LLP_website/actions/workflows/ci.yml/badge.svg)
![Deploy](https://github.com/unknown-umt-07/Gangotri-firestone-LLP_website/actions/workflows/deploy-vercel.yml/badge.svg)

This repository contains the static and Flask templates for the Gangotri Firestone (Hexochems) website.

Quick start
1. Create and activate a Python virtual environment.
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
2. Install dependencies:
```powershell
pip install -r requirements.txt
```
3. Run the app:
```powershell
python app.py
```

Notes
- Do NOT commit `firebase_credentials.json`, `local_db.json`, or the `uploads/` folder. They are excluded via `.gitignore`.
- Use GitHub repository secrets or environment variables for production credentials.

License
This project is licensed under the MIT License — see `LICENSE`.
# Gangotri Firestone Website

A Flask-based company website for Gangotri Firestone LLP / Hexochems with:
- a public website for products, about, and contact pages
- an admin panel for managing inquiries and products
- local JSON storage with Firebase fallback support

## Features
- Home, Products, About, Contact, and 404 pages
- Product catalog and product detail pages
- Contact form that saves inquiries
- Admin login to manage inquiries and products
- Image upload support for product entries

## Requirements
- Python 3.10+
- pip

## Setup
1. Open the project folder:
   ```bash
   cd D:\Gangotri firestone\website
   ```
2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Run the website
```bash
python app.py
```

Then open:
- http://127.0.0.1:5000
- http://127.0.0.1:5000/admin

## Admin access
Default admin passcode:
```text
admin123
```

## Storage
- The app uses local JSON storage by default via local_db.json
- If Firebase credentials are available and enabled, it can use Firebase Firestore instead

## Project files
- app.py — main Flask app
- database.py — database wrapper for local/Firebase storage
- templates/ — HTML templates
- static/ — CSS, JavaScript, and images
- local_db.json — local data storage
