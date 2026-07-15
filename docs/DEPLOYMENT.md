# Deployment Guide

This guide explains how to enable automatic deployments and required repository settings.

## Vercel setup (recommended)

1. Create a Vercel project from this repository.
2. In the Vercel dashboard, copy the **Project ID** and **Organization ID** for the project.
3. Create a Vercel token and copy it.
4. In your GitHub repository, add three Actions secrets:
   - `VERCEL_TOKEN` — your Vercel token
   - `VERCEL_ORG_ID` — your Vercel organization ID
   - `VERCEL_PROJECT_ID` — your Vercel project ID

   You can add them via the web UI: Settings → Secrets and variables → Actions → New repository secret.

5. After adding secrets, pushing to `main` will trigger the `deploy-vercel.yml` workflow and publish the site to Vercel.

## GitHub Secrets via CLI

If you prefer the `gh` CLI, you can set secrets from your terminal:

```bash
gh secret set VERCEL_TOKEN --body "<your-vercel-token>"
gh secret set VERCEL_ORG_ID --body "<your-vercel-org-id>"
gh secret set VERCEL_PROJECT_ID --body "<your-vercel-project-id>"
```

## Notes
- The deploy workflow will fail if secrets are missing.
- For production, ensure `FLASK_SECRET_KEY` and `ADMIN_PASSCODE` are also set as GitHub Actions secrets or environment variables on your hosting platform.
