# Deployment Guide

This guide explains how to enable automatic deployments and required repository settings.

## Render deployment (recommended)

1. Create a Render service from this repository.
2. In the Render dashboard, copy your service ID and create an API key.
3. In your GitHub repository, add two Actions secrets:
   - `RENDER_API_KEY` — your Render API key
   - `RENDER_SERVICE_ID` — your Render service ID

   You can add them via the web UI: Settings → Secrets and variables → Actions → New repository secret.

4. After adding secrets, pushing to `main` will trigger the `deploy-render.yml` workflow and publish the site to Render.

## Recommended Render service configuration

When creating the Render Web Service for this Flask app, use these settings to avoid runtime build problems:

- **Runtime / Python version**: set to `3.11` (for example `3.11.4`) — some binary wheels (cffi/eventlet) are most compatible with 3.11.
- **Build command**:

```bash
python -m pip install -U pip setuptools wheel
pip install -r requirements.txt
```

- **Start command** (used by Render to run the app):

```bash
gunicorn -k eventlet -w 1 app:app
```

- **Environment variables** (Render → Environment):
   - `FLASK_SECRET_KEY` — set to a secure random string (or use the generated value)
   - `ADMIN_PASSCODE` — e.g. `admin123` (change for production)
   - `USE_FIREBASE` — `true` or `false` depending on whether you provide Firebase credentials

Notes:
- Using the `-k eventlet` worker ensures Flask-SocketIO works correctly with Gunicorn. Without it you may see import or runtime errors in production.
- If you still see build errors referencing compiled modules (for example `No module named '_cffi_backend'`), make sure the Python version and the pip build steps above are used so wheels are installed correctly.

## GitHub Secrets via CLI

If you prefer the `gh` CLI, you can set secrets from your terminal:

```bash
gh secret set RENDER_API_KEY --body "<your-render-api-key>"
gh secret set RENDER_SERVICE_ID --body "<your-render-service-id>"
```

## Notes
- The deploy workflow will fail if secrets are missing.
- For production, ensure `FLASK_SECRET_KEY` and `ADMIN_PASSCODE` are also set as GitHub Actions secrets or environment variables on your hosting platform.
