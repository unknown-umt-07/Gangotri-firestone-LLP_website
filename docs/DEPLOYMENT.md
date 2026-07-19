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

## GitHub Secrets via CLI

If you prefer the `gh` CLI, you can set secrets from your terminal:

```bash
gh secret set RENDER_API_KEY --body "<your-render-api-key>"
gh secret set RENDER_SERVICE_ID --body "<your-render-service-id>"
```

## Notes
- The deploy workflow will fail if secrets are missing.
- For production, ensure `FLASK_SECRET_KEY` and `ADMIN_PASSCODE` are also set as GitHub Actions secrets or environment variables on your hosting platform.
