# LinkedIn Social Listening App - Carbon Measures

A free, open-source social listening application to monitor and analyze LinkedIn conversations around Carbon Measures (https://www.carbonmeasures.org/).

## Features

### 📊 Core Capabilities
- **Social Listening**: Monitor LinkedIn discussions about Carbon Measures
- **Engagement Analysis**: Track likes, comments, shares, and calculate engagement scores
- **Reach Estimation**: Estimate the reach of top-performing posts
- **Topic Clustering**: Automatically identify key themes in discussions using ML
- **Sentiment Analysis**: Analyze sentiment (positive, neutral, negative) for posts and clusters
- **Visual Analytics**: Interactive charts and graphs using Plotly
- **Export**: Download analysis results in CSV and JSON formats

### 🎯 Key Metrics
- Total engagement tracking
- Top performing posts identification
- Engagement trends over time
- Topic distribution analysis
- Sentiment breakdown by topic
- Estimated reach calculations

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone or download the files**
   ```bash
   # Create a project directory
   mkdir carbon-measures-listening
   cd carbon-measures-listening
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download TextBlob corpora** (required for sentiment analysis)
   ```bash
   python -m textblob.download_corpora
   ```

## Usage

### Running the App Locally

```bash
streamlit run linkedin_social_listening.py
```

The app will open in your browser at `http://localhost:8501`

### Running on Streamlit Cloud (FREE)

1. **Push to GitHub**
   - Create a new repository on GitHub
   - Upload `linkedin_social_listening.py` and `requirements.txt`

2. **Deploy on Streamlit Cloud**
   - Go to https://streamlit.io/cloud
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Deploy!

**Cost: $0** - Streamlit Community Cloud is completely free

## Data Sources

### Option 1: Demo Data (Included)
The app includes sample data for demonstration purposes. Select "Demo Data" in the sidebar to use it immediately.

### Option 2: Upload CSV
Prepare a CSV file with LinkedIn data in the following format:

| Column | Description | Example |
|--------|-------------|---------|
| post_id | Unique identifier | "post_001" |
| author | Author name | "Sarah Johnson" |
| title | Professional title | "Climate Solutions Architect" |
| text | Post content | "Just attended..." |
| likes | Number of likes | 245 |
| comments | Number of comments | 32 |
| shares | Number of shares | 18 |
| date | Post date | "2024-02-01" |
| url | LinkedIn URL | "https://linkedin.com/post/..." |

### Option 3: LinkedIn Data Collection

⚠️ **Important**: Always comply with LinkedIn's Terms of Service

#### Method A: LinkedIn API (Recommended)
- Apply for official LinkedIn API access
- Use OAuth 2.0 authentication
- Query posts using the Marketing API or Community Management API
- Cost: Free tier available, paid plans for higher volume
- **Best for**: Official, compliant, long-term solutions

#### Method B: Manual Export
1. Search for "Carbon Measures" on LinkedIn
2. Manually collect post data
3. Format as CSV
4. Upload to the app
- Cost: Free (time-intensive)
- **Best for**: Small-scale monitoring, proof of concept

#### Method C: Third-party Tools
Popular options:
- **Phantombuster**: LinkedIn scrapers with free tier
- **Apify**: Web scraping platform with LinkedIn actors
- **Octoparse**: Visual web scraping tool
- Cost: Free tiers available, paid plans for scale
- **Best for**: Medium-scale monitoring

## Technical Details

### Technologies Used
All free and open-source:
- **Streamlit**: Web app framework
- **Pandas**: Data manipulation
- **Scikit-learn**: Machine learning (clustering)
- **TextBlob**: Sentiment analysis
- **Plotly**: Interactive visualizations
- **NumPy**: Numerical computing

### Machine Learning Features

#### Topic Clustering
- **Algorithm**: K-Means clustering
- **Features**: TF-IDF vectorization
- **Output**: Automatic grouping of similar posts
- **Customizable**: Adjust number of clusters (2-5)

#### Sentiment Analysis
- **Library**: TextBlob
- **Method**: Pattern-based sentiment analysis
- **Scoring**: Polarity score from -1 (negative) to +1 (positive)
- **Categories**: Positive (>0.1), Neutral (-0.1 to 0.1), Negative (<-0.1)

#### Engagement Scoring
```python
Engagement Score = Likes + (Comments × 2) + (Shares × 3)
```
- Weights reflect the increasing value of deeper engagement
- Used to identify top-performing content

#### Reach Estimation
```python
Estimated Reach = Engagement Score × 10
```
- Simplified model based on typical LinkedIn reach multipliers
- Can be customized based on your audience data

## Visualizations

The app includes:
1. **Top Posts Rankings**: Identify highest-performing content
2. **Engagement Bar Charts**: Compare post performance
3. **Timeline Analysis**: Track engagement trends
4. **Topic Scatter Plot**: Visualize clusters and engagement
5. **Sentiment Pie Charts**: Overall and by-topic sentiment
6. **Topic Distribution**: Understand conversation themes

## Customization

### Adjusting Clusters
Use the sidebar slider to change the number of topic clusters (2-5).

### Modifying Engagement Weights
Edit line 99 in `linkedin_social_listening.py`:
```python
df['engagement_score'] = df['likes'] + (df['comments'] * 2) + (df['shares'] * 3)
```

### Changing Sentiment Thresholds
Edit lines 107-113 to adjust sensitivity:
```python
if polarity > 0.1:  # Change threshold
    return 'Positive', polarity
elif polarity < -0.1:  # Change threshold
    return 'Negative', polarity
```

## Cost Breakdown

| Component | Cost |
|-----------|------|
| Python | Free |
| Streamlit Community Cloud | Free |
| All Python libraries | Free (open-source) |
| **Total** | **$0** |

### Optional Costs
- LinkedIn API: Free tier available
- Data collection tools: Free tiers available (Phantombuster, Apify)
- Premium hosting: ~$7-20/month (if you outgrow free tier)

## Limitations

1. **LinkedIn API Access**: Requires application and approval
2. **Rate Limits**: Free tiers have usage limits
3. **Historical Data**: Limited by API or manual collection
4. **Real-time Updates**: Not automatically refreshing (refresh manually)
5. **Sentiment Accuracy**: Basic NLP; may miss context/sarcasm

## Future Enhancements

Potential additions:
- [ ] Automated LinkedIn API integration
- [ ] Real-time data refresh
- [ ] Advanced NLP (BERT, GPT-based sentiment)
- [ ] Network analysis (who's talking to whom)
- [ ] Competitor comparison
- [ ] Email alerts for trending posts
- [ ] Historical trend analysis
- [ ] Influencer identification

## Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### TextBlob sentiment error
```bash
python -m textblob.download_corpora
```

### Streamlit port already in use
```bash
streamlit run linkedin_social_listening.py --server.port 8502
```

### CSV upload not working
- Check CSV format matches expected columns
- Ensure date format is YYYY-MM-DD
- Verify no special characters in text fields

## License

MIT License - feel free to modify and use for commercial purposes.

## Contributing

Contributions welcome! Areas for improvement:
- LinkedIn API integration
- Advanced analytics
- Better sentiment models
- Additional visualizations
- Performance optimization

## Support

For issues or questions:
1. Check this README
2. Review the code comments
3. Test with demo data first
4. Verify LinkedIn API credentials (if using)

## Disclaimer

This tool is for educational and research purposes. Always comply with:
- LinkedIn Terms of Service
- Data privacy regulations (GDPR, CCPA)
- Ethical web scraping practices
- Copyright and intellectual property laws

---

**Built with ❤️ for Carbon Measures monitoring**
