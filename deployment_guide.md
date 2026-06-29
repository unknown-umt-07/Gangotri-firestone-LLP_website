# Gangotri Firestone (Hexochems) - Render Deployment Guide

Follow these steps to deploy your Flask web application live on **Render** using your **Firebase Firestore** database.

---

## Prerequisites

1. A **GitHub account** ([github.com](https://github.com/))
2. A **Render account** ([render.com](https://render.com/))
3. Your code files inside the `website/` subdirectory are clean and test suite runs correctly.

---

## Step 1: Upload the Code to GitHub

Since Render deploys directly from GitHub, you need to push your local files (including the `website/` directory and `render.yaml` configuration) to a GitHub repository.

### Option A: Using Git CLI (Command Line)
Open your terminal at the project root directory (`d:\Gangotri firestone`) and run:

```bash
# 1. Initialize git repository
git init

# 2. Create a .gitignore file at the root with:
# website/.venv/
# website/__pycache__/
# website/*.log
# website/local_db.json
# TEST - MSDS/
# TEST REPORT/
# *.pdf

# 3. Add files
git add .

# 4. Commit files
git commit -m "Configure subdirectory deployment and resolve bug fixes"

# 5. Link to GitHub (Replace with your actual GitHub repo URL)
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/gangotri-firestone.git

# 6. Push to GitHub
git push -u origin main
```

### Option B: Using GitHub Desktop (Highly Recommended on Windows)
1. Download and install **GitHub Desktop** from [desktop.github.com](https://desktop.github.com/).
2. Open the app and select **File** > **Add Local Repository**.
3. Choose the root directory `d:\Gangotri firestone` and click **Add Repository**.
4. Set up a `.gitignore` if asked (ignore `website/.venv` and `website/__pycache__`).
5. Write a commit message (e.g., "Ready for launch"), click **Commit to main**.
6. Click **Publish Repository** to upload the code to your GitHub account.

---

## Step 2: Create a Web Service on Render

1. Log into the **Render Dashboard** ([dashboard.render.com](https://dashboard.render.com/)).
2. Click **New +** in the top-right corner and select **Blueprint**. (Alternatively, you can select **Web Service**).
3. Connect your GitHub repository `gangotri-firestone`.
4. Render will automatically detect the settings from `render.yaml` in the root!
   - **Root Directory**: `website` (Automatically configured)
   - **Name**: `gangotri-firestone-llp`
   - **Runtime**: `Python`
   - **Build Command**: `pip install -r requirements.txt` (executed inside the `website` directory)
   - **Start Command**: `gunicorn app:app` (executed inside the `website` directory)
   - **Instance Type**: `Free`

---

## Step 3: Configure Environment Variables on Render

Before clicking deploy, navigate to the **Environment** tab inside your Render Web Service configurations and add:

| Key | Value | Description |
| :--- | :--- | :--- |
| `USE_FIREBASE` | `true` | Tells the database module to connect to Firestore rather than local JSON |
| `ADMIN_PASSCODE` | `your_custom_admin_password` | The passcode required to access `/admin` (Default: `admin123`) |
| `FLASK_SECRET_KEY` | `some_long_random_string` | Keeps user authentication sessions secure |

---

## Step 4: Handle Firebase Service Credentials

Since the service account file `firebase_credentials.json` contains private keys, you should **NOT** commit it directly to your GitHub repository.

### How to configure credentials securely on Render:
1. Open `website/firebase_credentials.json` locally and copy its entire text contents.
2. In the Render Dashboard under **Environment** variables for your Web Service:
   - Click **Add File** (or **Secret File**).
   - Set the Filename to: `firebase_credentials.json` (Since Render runs inside the `website` rootDirectory, this file will be automatically placed in the correct location).
   - Paste the copied JSON text contents into the value box.
   - Save changes.
3. Render will securely inject this file into your application workspace directory at runtime.

---

## Step 5: Test the Live Application

1. Render will initiate the deployment process, build the dependencies, and start the Gunicorn server.
2. Once the logs show `Your service is live`, copy the live URL provided by Render (e.g. `https://gangotri-firestone-llp.onrender.com`).
3. Visit the URL to test:
   - Browse the products.
   - Click "Inquire About This Product" and submit an inquiry.
   - Access `/admin` using your configured `ADMIN_PASSCODE` and check if inquiries populate successfully!
