# Deployment Guide: Streamlit Cloud

## Quick Start - Deploy in 5 Minutes (FREE)

### Step 1: Prepare Your GitHub Repository

1. **Create a new repository on GitHub**
   - Go to https://github.com/new
   - Name it: `carbon-measures-listening` (or any name you prefer)
   - Make it Public (required for free Streamlit Cloud)
   - Click "Create repository"

2. **Upload your files**
   Upload these three files to your repository:
   - `linkedin_social_listening.py`
   - `requirements.txt`
   - `README.md`
   
   You can drag and drop them via the GitHub web interface.

### Step 2: Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud**
   - Visit: https://streamlit.io/cloud
   - Click "Sign up" or "Sign in"
   - Authorize with your GitHub account

2. **Create a new app**
   - Click "New app" button
   - Select your repository: `carbon-measures-listening`
   - Branch: `main` (or `master`)
   - Main file path: `linkedin_social_listening.py`
   - Click "Deploy!"

3. **Wait for deployment** (usually 1-2 minutes)
   - Streamlit will install dependencies
   - Your app will automatically launch

4. **Access your app**
   - You'll get a URL like: `https://[your-app-name].streamlit.app`
   - Share this URL with anyone!

### Step 3: Configure (Optional)

**Custom Domain** (free)
- Go to app settings
- Add custom subdomain: `carbon-measures-[yourname].streamlit.app`

**Secrets Management** (for API keys)
- Click "Settings" → "Secrets"
- Add any API keys or credentials
- Format:
  ```toml
  # .streamlit/secrets.toml
  LINKEDIN_API_KEY = "your-key-here"
  ```

### Step 4: Update Your App

To update your app after deployment:

1. Make changes to your code locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update analysis features"
   git push
   ```
3. Streamlit Cloud auto-deploys new changes!

## Cost: $0

Streamlit Community Cloud is completely free and includes:
- ✅ Unlimited public apps
- ✅ 1 GB RAM per app
- ✅ Automatic HTTPS
- ✅ Subdomain hosting
- ✅ Auto-deployment from GitHub
- ✅ Community support

## Limitations of Free Tier

- Apps sleep after 7 days of inactivity (wake on first visit)
- 1 GB memory limit (sufficient for this app)
- Public repositories only
- No custom root domains (can use subdomains)

## Upgrade Options

If you need more:

**Streamlit Cloud Teams** ($20/month)
- Private repositories
- 4 GB RAM per app
- Always-on apps (no sleep)
- Priority support

**Streamlit Cloud Enterprise** (Custom pricing)
- Self-hosted option
- SSO/SAML
- Advanced security
- Dedicated support

## Alternative Hosting (Also Free)

### Option 1: Heroku
- Free tier available
- More complex setup
- Good for custom domains

### Option 2: Railway
- $5/month credit (free tier)
- Simple deployment
- GitHub integration

### Option 3: Google Cloud Run
- Free tier: 2M requests/month
- Auto-scaling
- More technical setup

### Option 4: Local Network
```bash
# Run on your local network
streamlit run linkedin_social_listening.py --server.address 0.0.0.0
```
Access from any device on your network at `http://[your-ip]:8501`

## Monitoring Your App

### View Logs
- In Streamlit Cloud dashboard
- Click your app → "Manage app" → "Logs"
- Real-time error tracking

### Analytics
- Streamlit Cloud provides basic analytics:
  - Number of views
  - Active users
  - Memory usage

### Custom Analytics
Add to your app:
```python
# Add to linkedin_social_listening.py
import streamlit as st

# Track page views
if 'page_views' not in st.session_state:
    st.session_state.page_views = 0
st.session_state.page_views += 1
```

## Security Best Practices

### 1. Never commit API keys
Use Streamlit secrets:
```python
import streamlit as st

# Access secrets
api_key = st.secrets["LINKEDIN_API_KEY"]
```

### 2. Validate user inputs
```python
uploaded_file = st.file_uploader("Upload CSV")
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        # Validate columns
        required_cols = ['post_id', 'author', 'text']
        if all(col in df.columns for col in required_cols):
            # Process data
            pass
    except Exception as e:
        st.error("Invalid CSV format")
```

### 3. Rate limiting
```python
import time
from datetime import datetime

if 'last_request' not in st.session_state:
    st.session_state.last_request = datetime.now()

time_since = (datetime.now() - st.session_state.last_request).seconds
if time_since < 5:  # 5 second cooldown
    st.warning("Please wait before making another request")
```

## Troubleshooting Deployment

### Error: "Requirements.txt not found"
- Ensure `requirements.txt` is in root directory
- Check file name is exact: `requirements.txt`

### Error: "Module not found"
- Add missing package to `requirements.txt`
- Exact version numbers help: `streamlit==1.31.0`

### Error: "Memory exceeded"
- Reduce dataset size
- Optimize code for memory
- Consider upgrading to Teams tier

### App is slow
- Profile your code
- Use `@st.cache_data` for expensive operations:
  ```python
  @st.cache_data
  def load_data():
      return pd.read_csv('data.csv')
  ```

### Port already in use (local)
```bash
# Use different port
streamlit run linkedin_social_listening.py --server.port 8502
```

## Performance Optimization

### Caching
```python
@st.cache_data
def calculate_engagement_metrics(df):
    # Expensive calculation
    return df

@st.cache_resource
def load_ml_model():
    # Load model once
    return model
```

### Session State
```python
# Store data in session
if 'data' not in st.session_state:
    st.session_state.data = load_data()

# Use cached data
df = st.session_state.data
```

## Next Steps

After deployment:
1. Test all features
2. Share URL with stakeholders
3. Monitor logs for errors
4. Gather user feedback
5. Iterate and improve

## Support

- **Streamlit Docs**: https://docs.streamlit.io
- **Community Forum**: https://discuss.streamlit.io
- **GitHub Issues**: Report bugs in your repo

---

**Deployment complete! Your app is now live and accessible worldwide.** 🚀
