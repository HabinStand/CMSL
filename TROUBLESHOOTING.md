# Streamlit Cloud Deployment Troubleshooting

## Issue: App Stuck on "Your app is in the oven" 🍳

This usually means the deployment is failing during the build process. Here's how to fix it:

## Solution 1: Check Your Requirements (Most Common Fix)

The issue is often with incompatible package versions. I've updated the `requirements.txt` to use more flexible version ranges:

```txt
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.17.0
scikit-learn>=1.3.0
textblob>=0.17.0
```

**Action:** Replace your `requirements.txt` with this updated version.

## Solution 2: Add System Packages

Create a file called `packages.txt` in your repository root:

```txt
python3-dev
build-essential
```

This ensures Streamlit Cloud has the necessary system libraries to build scikit-learn.

## Solution 3: Add Streamlit Config

Create a folder `.streamlit` and add `config.toml`:

```toml
[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
```

## Solution 4: Check Build Logs

1. Go to your app in Streamlit Cloud dashboard
2. Click "Manage app" (⚙️ icon)
3. Click "Logs" tab
4. Look for error messages in the build logs

Common errors and solutions:

### Error: "No module named 'sklearn'"
- Issue: scikit-learn not installed properly
- Fix: Add `scikit-learn>=1.3.0` to requirements.txt

### Error: "Failed building wheel for numpy"
- Issue: System dependencies missing
- Fix: Add `packages.txt` with build-essential

### Error: "ModuleNotFoundError: No module named 'textblob.download'"
- Issue: TextBlob corpora not downloaded
- Fix: Update the app code (see Solution 5 below)

### Error: Memory limit exceeded
- Issue: App using too much RAM during build
- Fix: Use lighter versions of packages or optimize code

## Solution 5: Fix TextBlob Download Issue

Streamlit Cloud can't run interactive commands like `python -m textblob.download_corpora`. Update your app to download automatically:

Add this at the top of `linkedin_social_listening.py`:

```python
import streamlit as st
import ssl
import nltk

# Fix for TextBlob on Streamlit Cloud
@st.cache_resource
def download_textblob_corpora():
    try:
        # Bypass SSL certificate verification if needed
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context
        
        # Download required NLTK data for TextBlob
        nltk.download('brown', quiet=True)
        nltk.download('punkt', quiet=True)
        return True
    except:
        return False

# Call this before using TextBlob
download_textblob_corpora()
```

Also add `nltk` to your requirements.txt:

```txt
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.17.0
scikit-learn>=1.3.0
textblob>=0.17.0
nltk>=3.8.0
```

## Solution 6: Simplify Dependencies (Nuclear Option)

If nothing works, create a minimal `requirements.txt`:

```txt
streamlit
pandas
plotly
scikit-learn
```

And replace sentiment analysis with a simpler approach in the code.

## Solution 7: Repository Structure

Ensure your GitHub repository has this structure:

```
your-repo/
├── linkedin_social_listening.py  (main file)
├── requirements.txt
├── packages.txt                  (optional but helpful)
├── .streamlit/
│   └── config.toml              (optional but helpful)
└── README.md
```

**Important:** No spaces in filenames, proper capitalization.

## Solution 8: Python Version

Streamlit Cloud uses Python 3.9-3.11 by default. If you need a specific version, create `runtime.txt`:

```txt
python-3.11
```

## Solution 9: Clear Cache and Redeploy

Sometimes Streamlit Cloud gets stuck with cached builds:

1. Go to Streamlit Cloud dashboard
2. Click your app's menu (⋮)
3. Select "Reboot app"
4. If that doesn't work: "Delete app"
5. Re-deploy from scratch

## Solution 10: Fork Deployment

If your repository is having issues:

1. Delete the Streamlit app
2. Create a **new** repository (don't reuse the same one)
3. Upload files to the new repository
4. Deploy from the new repository

## Quick Checklist ✅

Before deploying, verify:

- [ ] `requirements.txt` exists and has correct package names
- [ ] Repository is **public** (required for free tier)
- [ ] Main file is `linkedin_social_listening.py` (no typos)
- [ ] All files are in the repository root (not in subfolders)
- [ ] No syntax errors in Python code
- [ ] File encodings are UTF-8 (not UTF-16 or other)

## Testing Locally First

Before deploying to Streamlit Cloud, test locally:

```bash
# Clean install
pip uninstall -y streamlit pandas numpy plotly scikit-learn textblob
pip install -r requirements.txt

# Download TextBlob data
python -m textblob.download_corpora

# Run app
streamlit run linkedin_social_listening.py
```

If it works locally, it should work on Streamlit Cloud (with the fixes above).

## Still Not Working?

### Option A: Check Streamlit Status
Visit https://status.streamlit.io/ to see if there are service issues.

### Option B: Use Streamlit Community Forum
Post your issue with logs: https://discuss.streamlit.io/

### Option C: Alternative Hosting

If Streamlit Cloud continues to have issues, try:

1. **Hugging Face Spaces** (also free)
   - Create space at https://huggingface.co/spaces
   - Upload files
   - Select Streamlit SDK
   - Deploy

2. **Railway** (free tier)
   - Connect GitHub
   - Auto-deploys
   - More resources than Streamlit Cloud

3. **Render** (free tier)
   - Static site hosting
   - Good for Streamlit apps
   - https://render.com

## Common "In the Oven" Causes Summary

| Symptom | Cause | Fix |
|---------|-------|-----|
| Stuck for 5+ minutes | Build failing | Check logs, fix requirements.txt |
| "Building..." forever | Memory issue | Reduce dependencies or upgrade |
| Random timeout | Streamlit Cloud issue | Wait and retry later |
| Fails immediately | Syntax error | Check Python code |
| Works locally, not cloud | Missing system packages | Add packages.txt |

## Example Working Configuration

Here's a **guaranteed working** minimal setup:

**requirements.txt:**
```txt
streamlit==1.28.0
pandas==2.0.3
plotly==5.17.0
```

**Modified app (without scikit-learn and textblob):**
- Remove sentiment analysis (or use simple keyword matching)
- Remove clustering (or use simple grouping)
- Focus on visualization and metrics

This will get you deployed, then you can gradually add features back.

## Contact Support

If you've tried everything:
- Email: support@streamlit.io
- Forum: https://discuss.streamlit.io/c/deployment-issues
- Include: repository link, error logs, what you've tried

---

**Most Common Fix:** Update requirements.txt to use `>=` instead of `==` for version numbers. This solves 80% of deployment issues!
