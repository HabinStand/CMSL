import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from textblob import TextBlob
import re
from collections import Counter
import json

# Page configuration
st.set_page_config(
    page_title="LinkedIn Social Listening - Carbon Measures",
    page_icon="🌍",
    layout="wide"
)

# Title and description
st.title("🌍 LinkedIn Social Listening: Carbon Measures")
st.markdown("Monitor and analyze LinkedIn conversations around [Carbon Measures](https://www.carbonmeasures.org/)")

# Sidebar for configuration
st.sidebar.header("⚙️ Configuration")
st.sidebar.markdown("""
**Note:** This app demonstrates the analysis pipeline. 

To capture real LinkedIn data, you would need:
- LinkedIn API access (requires approval)
- Or use web scraping (with LinkedIn's permission)
- Or manual data import from LinkedIn exports
""")

# Sample data generator for demonstration
def generate_sample_data():
    """Generate sample LinkedIn posts about Carbon Measures"""
    sample_posts = [
        {
            "post_id": "post_001",
            "author": "Sarah Johnson",
            "title": "Climate Solutions Architect",
            "text": "Just attended the Carbon Measures summit. Their approach to standardizing carbon accounting is revolutionary! #CarbonMeasures #ClimateAction",
            "likes": 245,
            "comments": 32,
            "shares": 18,
            "date": datetime.now() - timedelta(days=2),
            "url": "https://linkedin.com/post/001"
        },
        {
            "post_id": "post_002",
            "author": "Michael Chen",
            "title": "Sustainability Director",
            "text": "Carbon Measures methodology helps us track emissions accurately. Finally, a reliable framework for corporate carbon accounting.",
            "likes": 189,
            "comments": 21,
            "shares": 12,
            "date": datetime.now() - timedelta(days=5),
            "url": "https://linkedin.com/post/002"
        },
        {
            "post_id": "post_003",
            "author": "Emma Williams",
            "title": "ESG Analyst",
            "text": "Concerns about the complexity of Carbon Measures implementation. Need more guidance for SMEs. Anyone else facing challenges?",
            "likes": 67,
            "comments": 45,
            "shares": 8,
            "date": datetime.now() - timedelta(days=3),
            "url": "https://linkedin.com/post/003"
        },
        {
            "post_id": "post_004",
            "author": "David Brown",
            "title": "CFO",
            "text": "Carbon Measures is transforming how we report sustainability metrics to investors. Highly recommend for any serious ESG program.",
            "likes": 312,
            "comments": 54,
            "shares": 29,
            "date": datetime.now() - timedelta(days=1),
            "url": "https://linkedin.com/post/004"
        },
        {
            "post_id": "post_005",
            "author": "Lisa Anderson",
            "title": "Environmental Consultant",
            "text": "Working with Carbon Measures has streamlined our client reporting. The standardization is exactly what the industry needed.",
            "likes": 156,
            "comments": 28,
            "shares": 15,
            "date": datetime.now() - timedelta(days=4),
            "url": "https://linkedin.com/post/005"
        },
        {
            "post_id": "post_006",
            "author": "James Miller",
            "title": "VP Operations",
            "text": "Questions about Carbon Measures pricing structure. Would love to hear from others about ROI and implementation costs.",
            "likes": 93,
            "comments": 38,
            "shares": 6,
            "date": datetime.now() - timedelta(days=6),
            "url": "https://linkedin.com/post/006"
        },
        {
            "post_id": "post_007",
            "author": "Rachel Green",
            "title": "Chief Sustainability Officer",
            "text": "Carbon Measures certification achieved! Proud of our team for meeting these rigorous standards. #NetZero #Sustainability",
            "likes": 421,
            "comments": 67,
            "shares": 34,
            "date": datetime.now() - timedelta(hours=12),
            "url": "https://linkedin.com/post/007"
        },
        {
            "post_id": "post_008",
            "author": "Tom Wilson",
            "title": "Data Scientist",
            "text": "The data infrastructure behind Carbon Measures is impressive. Integration with existing systems was smoother than expected.",
            "likes": 178,
            "comments": 19,
            "shares": 11,
            "date": datetime.now() - timedelta(days=7),
            "url": "https://linkedin.com/post/008"
        },
        {
            "post_id": "post_009",
            "author": "Amanda Taylor",
            "title": "Procurement Manager",
            "text": "Using Carbon Measures to evaluate supplier emissions. Game-changer for sustainable procurement decisions.",
            "likes": 203,
            "comments": 25,
            "shares": 17,
            "date": datetime.now() - timedelta(days=3),
            "url": "https://linkedin.com/post/009"
        },
        {
            "post_id": "post_010",
            "author": "Kevin Martinez",
            "title": "Investment Analyst",
            "text": "Investors are increasingly asking about Carbon Measures compliance. This is becoming a key criterion for ESG investments.",
            "likes": 267,
            "comments": 41,
            "shares": 23,
            "date": datetime.now() - timedelta(days=2),
            "url": "https://linkedin.com/post/010"
        }
    ]
    return pd.DataFrame(sample_posts)

# Calculate engagement metrics
def calculate_engagement_metrics(df):
    """Calculate engagement score and reach metrics"""
    df['engagement_score'] = df['likes'] + (df['comments'] * 2) + (df['shares'] * 3)
    df['reach_estimate'] = df['engagement_score'] * 10  # Simplified reach estimation
    return df

# Sentiment analysis
def analyze_sentiment(text):
    """Analyze sentiment of text using TextBlob"""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    
    if polarity > 0.1:
        return 'Positive', polarity
    elif polarity < -0.1:
        return 'Negative', polarity
    else:
        return 'Neutral', polarity

# Topic clustering
def cluster_topics(texts, n_clusters=3):
    """Cluster posts into topics using TF-IDF and K-Means"""
    vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
    X = vectorizer.fit_transform(texts)
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(X)
    
    # Get top words for each cluster
    feature_names = vectorizer.get_feature_names_out()
    cluster_keywords = {}
    
    for i in range(n_clusters):
        cluster_center = kmeans.cluster_centers_[i]
        top_indices = cluster_center.argsort()[-5:][::-1]
        top_words = [feature_names[idx] for idx in top_indices]
        cluster_keywords[i] = top_words
    
    return clusters, cluster_keywords

# Main app logic
def main():
    # Data source selection
    data_source = st.sidebar.radio(
        "Data Source",
        ["Demo Data", "Upload CSV"]
    )
    
    if data_source == "Demo Data":
        df = generate_sample_data()
        st.sidebar.success("✅ Using demo data")
    else:
        uploaded_file = st.sidebar.file_uploader(
            "Upload LinkedIn data (CSV)", 
            type=['csv']
        )
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.sidebar.success("✅ Data uploaded")
        else:
            st.info("👆 Please upload a CSV file or select Demo Data")
            st.markdown("""
            ### Expected CSV format:
            - **post_id**: Unique identifier
            - **author**: Post author name
            - **title**: Author's professional title
            - **text**: Post content
            - **likes**: Number of likes
            - **comments**: Number of comments
            - **shares**: Number of shares
            - **date**: Post date (YYYY-MM-DD)
            - **url**: Post URL
            """)
            return
    
    # Calculate metrics
    df = calculate_engagement_metrics(df)
    
    # Add sentiment analysis
    sentiments = []
    sentiment_scores = []
    for text in df['text']:
        sentiment, score = analyze_sentiment(text)
        sentiments.append(sentiment)
        sentiment_scores.append(score)
    
    df['sentiment'] = sentiments
    df['sentiment_score'] = sentiment_scores
    
    # Clustering
    n_clusters = st.sidebar.slider("Number of topic clusters", 2, 5, 3)
    clusters, cluster_keywords = cluster_topics(df['text'].tolist(), n_clusters)
    df['cluster'] = clusters
    
    # Assign cluster names based on keywords
    cluster_names = {}
    for i, keywords in cluster_keywords.items():
        cluster_names[i] = f"Topic {i+1}: {', '.join(keywords[:3])}"
    df['cluster_name'] = df['cluster'].map(cluster_names)
    
    # Display metrics
    st.header("📊 Overview Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Posts", len(df))
    with col2:
        st.metric("Total Engagement", f"{df['engagement_score'].sum():,.0f}")
    with col3:
        st.metric("Avg. Engagement", f"{df['engagement_score'].mean():.0f}")
    with col4:
        st.metric("Est. Total Reach", f"{df['reach_estimate'].sum():,.0f}")
    
    # Top Posts Section
    st.header("🔥 Top Performing Posts")
    top_n = st.slider("Number of top posts to display", 3, 10, 5)
    
    top_posts = df.nlargest(top_n, 'engagement_score')[
        ['author', 'title', 'text', 'engagement_score', 'reach_estimate', 'sentiment', 'date', 'url']
    ]
    
    for idx, row in top_posts.iterrows():
        with st.expander(f"🏆 {row['author']} - {row['title']} (Engagement: {row['engagement_score']:.0f})"):
            st.write(f"**Posted:** {row['date'].strftime('%Y-%m-%d %H:%M')}")
            st.write(f"**Sentiment:** {row['sentiment']}")
            st.write(f"**Estimated Reach:** {row['reach_estimate']:,.0f}")
            st.write(f"**Text:** {row['text']}")
            st.write(f"🔗 [View on LinkedIn]({row['url']})")
    
    # Engagement visualization
    st.header("📈 Engagement Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_engagement = px.bar(
            df.nlargest(10, 'engagement_score'),
            x='author',
            y='engagement_score',
            color='sentiment',
            title="Top 10 Posts by Engagement Score",
            labels={'engagement_score': 'Engagement Score', 'author': 'Author'},
            color_discrete_map={'Positive': '#2ecc71', 'Neutral': '#95a5a6', 'Negative': '#e74c3c'}
        )
        fig_engagement.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_engagement, use_container_width=True)
    
    with col2:
        # Engagement over time
        df_sorted = df.sort_values('date')
        fig_timeline = px.line(
            df_sorted,
            x='date',
            y='engagement_score',
            title="Engagement Over Time",
            labels={'engagement_score': 'Engagement Score', 'date': 'Date'}
        )
        st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Topic Clustering
    st.header("🎯 Topic Clustering")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_clusters = px.scatter(
            df,
            x=range(len(df)),
            y='engagement_score',
            color='cluster_name',
            size='reach_estimate',
            hover_data=['author', 'text'],
            title="Posts by Topic Cluster",
            labels={'x': 'Post Index', 'engagement_score': 'Engagement Score'}
        )
        st.plotly_chart(fig_clusters, use_container_width=True)
    
    with col2:
        cluster_counts = df['cluster_name'].value_counts()
        fig_cluster_dist = px.pie(
            values=cluster_counts.values,
            names=cluster_counts.index,
            title="Topic Distribution"
        )
        st.plotly_chart(fig_cluster_dist, use_container_width=True)
    
    # Detailed cluster analysis
    st.subheader("Topic Details")
    for i in range(n_clusters):
        cluster_df = df[df['cluster'] == i]
        avg_sentiment = cluster_df['sentiment_score'].mean()
        
        with st.expander(f"{cluster_names[i]} ({len(cluster_df)} posts)"):
            st.write(f"**Average Sentiment Score:** {avg_sentiment:.3f}")
            st.write(f"**Total Engagement:** {cluster_df['engagement_score'].sum():,.0f}")
            st.write(f"**Key Terms:** {', '.join(cluster_keywords[i])}")
            
            # Show sample posts from cluster
            st.write("**Sample Posts:**")
            for _, post in cluster_df.head(3).iterrows():
                st.write(f"- *{post['author']}*: {post['text'][:100]}...")
    
    # Sentiment Analysis
    st.header("💭 Sentiment Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        sentiment_counts = df['sentiment'].value_counts()
        fig_sentiment = px.pie(
            values=sentiment_counts.values,
            names=sentiment_counts.index,
            title="Overall Sentiment Distribution",
            color=sentiment_counts.index,
            color_discrete_map={'Positive': '#2ecc71', 'Neutral': '#95a5a6', 'Negative': '#e74c3c'}
        )
        st.plotly_chart(fig_sentiment, use_container_width=True)
    
    with col2:
        # Sentiment by cluster
        sentiment_cluster = df.groupby(['cluster_name', 'sentiment']).size().reset_index(name='count')
        fig_sentiment_cluster = px.bar(
            sentiment_cluster,
            x='cluster_name',
            y='count',
            color='sentiment',
            title="Sentiment by Topic Cluster",
            barmode='stack',
            color_discrete_map={'Positive': '#2ecc71', 'Neutral': '#95a5a6', 'Negative': '#e74c3c'}
        )
        fig_sentiment_cluster.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_sentiment_cluster, use_container_width=True)
    
    # Cluster-specific sentiment analysis
    st.subheader("Sentiment Analysis by Topic")
    
    for i in range(n_clusters):
        cluster_df = df[df['cluster'] == i]
        sentiment_breakdown = cluster_df['sentiment'].value_counts()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(cluster_names[i], f"{len(cluster_df)} posts")
        with col2:
            positive_pct = (sentiment_breakdown.get('Positive', 0) / len(cluster_df)) * 100
            st.metric("Positive", f"{positive_pct:.1f}%")
        with col3:
            neutral_pct = (sentiment_breakdown.get('Neutral', 0) / len(cluster_df)) * 100
            st.metric("Neutral", f"{neutral_pct:.1f}%")
        with col4:
            negative_pct = (sentiment_breakdown.get('Negative', 0) / len(cluster_df)) * 100
            st.metric("Negative", f"{negative_pct:.1f}%")
    
    # Export data
    st.header("💾 Export Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download Full Analysis (CSV)",
            data=csv,
            file_name=f"carbon_measures_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    with col2:
        # Create summary report
        summary = {
            "analysis_date": datetime.now().isoformat(),
            "total_posts": len(df),
            "total_engagement": int(df['engagement_score'].sum()),
            "average_engagement": float(df['engagement_score'].mean()),
            "sentiment_distribution": df['sentiment'].value_counts().to_dict(),
            "top_posts": top_posts[['author', 'engagement_score', 'sentiment']].to_dict('records'),
            "clusters": {cluster_names[i]: int((df['cluster'] == i).sum()) for i in range(n_clusters)}
        }
        
        json_summary = json.dumps(summary, indent=2)
        st.download_button(
            label="Download Summary (JSON)",
            data=json_summary,
            file_name=f"carbon_measures_summary_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    ### 📝 Notes on Implementation
    
    **Current Status:** This is a demo using sample data.
    
    **To capture real LinkedIn data:**
    
    1. **LinkedIn API** (Recommended)
       - Apply for LinkedIn API access
       - Use official endpoints for posts and analytics
       - Requires approval and compliance with LinkedIn's terms
    
    2. **Manual Export**
       - Export LinkedIn search results
       - Format as CSV matching the expected structure
       - Upload to this tool
    
    3. **Third-party Tools**
       - Use services like Phantombuster, Apify, or Octoparse
       - Ensure compliance with LinkedIn's ToS
       - May require paid subscriptions
    
    **Free Tools Used:**
    - Streamlit (free hosting on Streamlit Community Cloud)
    - Python libraries: pandas, scikit-learn, textblob, plotly
    - All open-source and free for commercial use
    """)

if __name__ == "__main__":
    main()
