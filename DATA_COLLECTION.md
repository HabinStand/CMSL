# LinkedIn Data Collection Guide

## Overview

This guide explains how to collect LinkedIn data for the Carbon Measures social listening app while respecting LinkedIn's Terms of Service and data privacy regulations.

## ⚠️ Important Legal Disclaimer

**Always comply with:**
- LinkedIn Terms of Service
- GDPR (Europe)
- CCPA (California)
- Local data privacy laws
- Ethical data collection practices

## Method 1: LinkedIn API (RECOMMENDED)

### Why LinkedIn API?
✅ Official and compliant  
✅ Reliable and stable  
✅ Structured data  
✅ No ToS violations  

### Prerequisites
- LinkedIn account
- Company page (for some APIs)
- Developer application approval

### Step-by-Step Setup

#### 1. Create LinkedIn Developer Account
1. Go to https://www.linkedin.com/developers/
2. Sign in with your LinkedIn account
3. Click "Create app"
4. Fill in application details:
   - App name: "Carbon Measures Social Listening"
   - LinkedIn Page: Your company page
   - App logo: Upload logo
   - Legal agreement: Check and accept

#### 2. Request API Access
1. Navigate to "Products" tab
2. Request access to:
   - **Marketing Developer Platform** (for posts)
   - **Community Management API** (for engagement)
3. Provide use case: "Social listening for brand monitoring"
4. Wait for approval (typically 1-7 days)

#### 3. Get API Credentials
1. Go to "Auth" tab
2. Note your:
   - Client ID
   - Client Secret
3. Add redirect URL: `http://localhost:8501` (for local testing)

#### 4. Implement OAuth 2.0

```python
import requests
from urllib.parse import urlencode

# Step 1: Get authorization code
auth_url = "https://www.linkedin.com/oauth/v2/authorization"
params = {
    "response_type": "code",
    "client_id": "YOUR_CLIENT_ID",
    "redirect_uri": "http://localhost:8501",
    "scope": "r_organization_social r_basicprofile"
}

# User visits this URL and authorizes
authorization_url = f"{auth_url}?{urlencode(params)}"
print(f"Visit: {authorization_url}")

# Step 2: Exchange code for access token
token_url = "https://www.linkedin.com/oauth/v2/accessToken"
code = "CODE_FROM_REDIRECT"  # Get from redirect

token_params = {
    "grant_type": "authorization_code",
    "code": code,
    "redirect_uri": "http://localhost:8501",
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET"
}

response = requests.post(token_url, data=token_params)
access_token = response.json()["access_token"]
```

#### 5. Search for Posts

```python
# Search for posts mentioning Carbon Measures
search_url = "https://api.linkedin.com/v2/posts:search"

headers = {
    "Authorization": f"Bearer {access_token}",
    "X-Restli-Protocol-Version": "2.0.0"
}

params = {
    "q": "search",
    "keywords": "Carbon Measures",
    "count": 50
}

response = requests.get(search_url, headers=headers, params=params)
posts = response.json()
```

#### 6. Get Engagement Metrics

```python
# Get post analytics
post_id = "urn:li:share:123456789"
analytics_url = f"https://api.linkedin.com/v2/socialActions/{post_id}"

response = requests.get(analytics_url, headers=headers)
engagement = response.json()

# Extract metrics
likes = engagement.get("likeCount", 0)
comments = engagement.get("commentCount", 0)
shares = engagement.get("shareCount", 0)
```

### API Limitations
- **Rate Limits**: Typically 100 requests/day (free tier)
- **Data Access**: Only public posts and pages you manage
- **Historical Data**: Limited to recent posts
- **Costs**: Free tier available, paid for higher volume

### Cost Structure
- **Free**: 100 API calls/day
- **Partner Program**: Contact LinkedIn for higher limits
- **Enterprise**: Custom pricing for large-scale access

## Method 2: Manual Collection

### Best For
- Small-scale monitoring
- Proof of concept
- When API access is pending

### Process

#### 1. LinkedIn Search
1. Go to LinkedIn
2. Search: "Carbon Measures"
3. Filter by "Posts" tab
4. Review relevant posts

#### 2. Data Recording Template
Create a spreadsheet with columns:
- Post URL
- Author name
- Author title
- Post text
- Date posted
- Likes count
- Comments count
- Shares count

#### 3. Manual Entry
- Copy each field into spreadsheet
- Be consistent with formatting
- Record date as YYYY-MM-DD

#### 4. Export as CSV
- Save spreadsheet as CSV
- Upload to the app

### Limitations
- ❌ Time-intensive
- ❌ Limited scalability
- ❌ Manual errors possible
- ❌ No automation

## Method 3: Third-Party Tools

### Option A: Phantombuster

**What it is:** Cloud-based automation platform

**Setup:**
1. Create account: https://phantombuster.com
2. Find "LinkedIn Post Likers" phantom
3. Configure search parameters
4. Export results

**Pricing:**
- Free tier: Limited executions
- Starter: $30/month
- Pro: $50/month

**Pros:**
✅ Easy setup  
✅ No coding required  
✅ Reliable execution  

**Cons:**
❌ Paid after free tier  
❌ Gray area with LinkedIn ToS  

### Option B: Apify

**What it is:** Web scraping platform

**Setup:**
1. Account: https://apify.com
2. Use "LinkedIn Scraper" actor
3. Configure search: "Carbon Measures"
4. Download results

**Pricing:**
- Free tier: $5 credit
- Personal: $49/month
- Team: $499/month

**Pros:**
✅ Powerful scraping  
✅ Good documentation  
✅ Data quality  

**Cons:**
❌ Technical learning curve  
❌ Paid for scale  

### Option C: Octoparse

**What it is:** Visual web scraping tool

**Setup:**
1. Download: https://www.octoparse.com
2. Create task for LinkedIn
3. Configure selectors
4. Run and export

**Pricing:**
- Free: 10 tasks
- Standard: $75/month
- Professional: $209/month

**Pros:**
✅ Visual interface  
✅ No coding  
✅ Templates available  

**Cons:**
❌ Slower than API  
❌ May break with UI changes  

### ⚚ Third-Party Tool Cautions

**LinkedIn's Position:**
- Automated scraping violates ToS
- Use at your own risk
- Accounts may be restricted

**Best Practices:**
- Use rate limiting
- Respect robots.txt
- Don't overload servers
- Consider ethical implications

## Method 4: LinkedIn Sales Navigator

### What it is
Premium LinkedIn tool with advanced search and export features.

### Setup
1. Subscribe to Sales Navigator ($99/month)
2. Use advanced search for "Carbon Measures"
3. Save leads mentioning topic
4. Export to CRM/CSV

### Limitations
- ❌ Expensive
- ❌ Limited post data
- ❌ Focused on people, not content
- ✅ Official LinkedIn product

## Method 5: RSS/Email Alerts

### Google Alerts
1. Create alert: "site:linkedin.com Carbon Measures"
2. Receive daily/weekly emails
3. Manually compile data

### LinkedIn Notifications
1. Follow hashtag: #CarbonMeasures
2. Turn on post notifications
3. Manually track engagement

### Limitations
- ❌ Manual compilation
- ❌ No automation
- ❌ Limited to new posts
- ✅ Free and simple

## Data Privacy Compliance

### GDPR Requirements (EU)
If collecting data on EU residents:
- ✅ Have lawful basis (legitimate interest)
- ✅ Provide privacy notice
- ✅ Enable data deletion requests
- ✅ Implement data security
- ✅ Report breaches within 72 hours

### CCPA Requirements (California)
- ✅ Disclose data collection
- ✅ Allow opt-out
- ✅ Don't sell personal data
- ✅ Respond to consumer requests

### Best Practices
1. **Collect only public data**
2. **Anonymize when possible**
3. **Secure data storage**
4. **Delete when no longer needed**
5. **Document your processes**

## Ethical Considerations

### DO:
✅ Focus on public posts  
✅ Respect user privacy  
✅ Use data for legitimate business purposes  
✅ Follow platform rules  
✅ Be transparent about monitoring  

### DON'T:
❌ Collect private messages  
❌ Scrape personal information  
❌ Use for harassment or spam  
❌ Violate terms of service  
❌ Share data inappropriately  

## Integration with the App

### Using API Data

```python
# In linkedin_social_listening.py

def fetch_linkedin_data(access_token, keyword="Carbon Measures"):
    """Fetch posts from LinkedIn API"""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Restli-Protocol-Version": "2.0.0"
    }
    
    # Search for posts
    search_url = "https://api.linkedin.com/v2/posts:search"
    params = {"q": "search", "keywords": keyword, "count": 100}
    
    response = requests.get(search_url, headers=headers, params=params)
    posts = response.json().get("elements", [])
    
    # Transform to DataFrame
    data = []
    for post in posts:
        data.append({
            "post_id": post["id"],
            "author": post["author"]["name"],
            "text": post["text"],
            "likes": post["likeCount"],
            "comments": post["commentCount"],
            "shares": post["shareCount"],
            "date": post["publishedAt"],
            "url": post["permalink"]
        })
    
    return pd.DataFrame(data)

# Add to sidebar
if st.sidebar.checkbox("Connect LinkedIn API"):
    access_token = st.sidebar.text_input("Access Token", type="password")
    if access_token:
        df = fetch_linkedin_data(access_token)
```

### Using CSV Upload
Already implemented in the app - just prepare CSV with correct format.

## Recommended Approach

### For Beginners
1. Start with **manual collection**
2. Test with demo data
3. Refine your analytics

### For Small Teams
1. Apply for **LinkedIn API**
2. Use while waiting for approval: manual collection
3. Automate once approved

### For Agencies/Enterprises
1. **LinkedIn API** + **Partner Program**
2. Consider **third-party tools** as backup
3. Implement **data governance** policies

## Troubleshooting

### API Application Rejected
- Provide more detailed use case
- Show legitimate business need
- Reapply after improving application

### Rate Limit Exceeded
- Reduce request frequency
- Cache results
- Consider paid tier

### Data Quality Issues
- Validate data before analysis
- Handle missing fields gracefully
- Clean text data (remove emojis, etc.)

## Resources

### Official Documentation
- LinkedIn API: https://docs.microsoft.com/en-us/linkedin/
- Marketing API: https://docs.microsoft.com/en-us/linkedin/marketing/
- OAuth 2.0: https://docs.microsoft.com/en-us/linkedin/shared/authentication/

### Tools
- Postman: Test API calls
- Python `requests`: API integration
- `linkedin-api` library: Unofficial Python wrapper

### Legal
- LinkedIn ToS: https://www.linkedin.com/legal/user-agreement
- GDPR: https://gdpr.eu/
- CCPA: https://oag.ca.gov/privacy/ccpa

## Support

For questions about:
- **LinkedIn API**: https://linkedin.com/developers/support
- **This app**: See main README.md
- **Legal compliance**: Consult a lawyer (this is not legal advice)

---

**Remember: When in doubt, choose the most compliant and ethical approach.** The goal is sustainable, long-term monitoring that respects user privacy and platform rules.
