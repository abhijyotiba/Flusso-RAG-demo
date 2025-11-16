# Flusso RAG Demo - Security Update

## 🚨 URGENT: API Key Leaked and Revoked

Your API key was detected in the GitHub repository and has been automatically revoked by Google.

## Immediate Actions Required:

### 1. Get a New API Key
- Visit: https://aistudio.google.com/apikey
- Create a new API key
- **DO NOT commit it to GitHub**

### 2. Set Up Environment Variables Locally
```bash
# Copy the example file
copy .env.example .env

# Edit .env and add your NEW API key
GEMINI_API_KEY=your_new_api_key_here
STORE_ID=fileSearchStores/flusso-complete-knowledge-b-n8g5l5u765nh
```

### 3. Configure Render Deployment
1. Go to: https://dashboard.render.com/
2. Select your `flusso-rag-demo` service
3. Go to "Environment" tab
4. Add/Update these environment variables:
   - `GEMINI_API_KEY` = your_new_api_key
   - `STORE_ID` = fileSearchStores/flusso-complete-knowledge-b-n8g5l5u765nh

### 4. Update GitHub Repository
```bash
# Stage security changes
git add .gitignore .env.example backend/app.py

# Commit the security fix
git commit -m "Security: Remove hardcoded API key, use environment variables only"

# Push to GitHub
git push origin main
```

### 5. Clean Git History (Optional but Recommended)
Your old API key is still in git history. To completely remove it:

```bash
# Install BFG Repo Cleaner or use git filter-branch
# WARNING: This rewrites history, coordinate with any collaborators

# Using BFG (easier):
# Download from: https://rtyley.github.io/bfg-repo-cleaner/
# Then run:
# bfg --replace-text passwords.txt  # Create passwords.txt with your old API key
# git reflog expire --expire=now --all && git gc --prune=now --aggressive
# git push --force
```

## What Changed:

- ✅ Removed hardcoded API key from `backend/app.py`
- ✅ Added `.env.example` with template
- ✅ Updated `.gitignore` to exclude `.env` files
- ✅ App now requires environment variables (fails fast if missing)

## Running Locally:
```bash
# Make sure .env exists with your new API key
python backend/app.py
```

## Why This Happened:
The API key was committed to the public GitHub repository in the file `backend/app.py`. GitHub and Google scan for exposed credentials and automatically revoke them for security.

## Best Practices Going Forward:
1. ✅ Always use `.env` files for secrets
2. ✅ Never commit `.env` files (add to `.gitignore`)
3. ✅ Use `.env.example` as a template (without real values)
4. ✅ Set environment variables in deployment platforms
5. ✅ Rotate API keys if ever exposed
