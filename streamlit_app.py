import streamlit as st
from datetime import datetime

# Configure the page
st.set_page_config(
    page_title="Knead Strategy Forum",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Force dark theme and styling
st.markdown("""
<style>
    /* Dark Theme */
    body {
        color: white;
        background-color: #111827;
    }
    
    /* Header Style */
    .header-container {
        background-color: #6c3ce9;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    .header-title {
        color: white;
        font-size: 32px;
        font-weight: bold;
    }
    
    /* Strategy Card */
    .strategy-card {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        position: relative;
    }
    
    .strategy-title {
        color: #333;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 5px;
    }
    
    .strategy-author {
        color: #555;
        font-size: 14px;
        margin-bottom: 15px;
    }
    
    .strategy-description {
        color: #333;
        margin-bottom: 15px;
    }
    
    .strategy-meta {
        display: flex;
        justify-content: space-between;
        color: #666;
        font-size: 14px;
    }
    
    .like-count {
        position: absolute;
        top: 20px;
        right: 20px;
        color: #666;
        font-size: 18px;
    }
    
    /* Buttons */
    .button-container {
        display: flex;
        gap: 10px;
        margin-top: 10px;
    }
    
    /* Override Streamlit Styles */
    .stButton button {
        border-radius: 5px;
        border: 1px solid #333;
        color: #333;
        background-color: transparent;
    }
    
    .stTextInput input {
        border-radius: 20px;
        background-color: #333;
        color: white;
        border: none;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'strategies' not in st.session_state:
    st.session_state.strategies = [
        {
            "id": "1",
            "title": "Moving Average Crossover Strategy",
            "description": "This strategy identifies trend reversals by tracking when shorter-term moving averages cross above or below longer-term moving averages. When the 50-day moving average crosses above the 200-day moving average (golden cross), it generates a buy signal. When the 50-day moving average crosses below the 200-day moving average (death cross), it generates a sell signal.",
            "author": "Sarah Johnson",
            "date": "2025-05-17T10:30:00Z",
            "likes": 42,
            "comments": 2
        },
        {
            "id": "2",
            "title": "RSI Divergence Trading",
            "description": "This strategy focuses on identifying divergences between price action and RSI indicator. When price makes a higher high but RSI makes a lower high (bearish divergence), it signals a potential trend reversal to the downside. Conversely, when price makes a lower low but RSI makes a higher low (bullish divergence), it signals a potential trend reversal to the upside.",
            "author": "Michael Brown",
            "date": "2025-05-15T15:45:00Z",
            "likes": 37,
            "comments": 2
        },
        {
            "id": "3",
            "title": "Ichimoku Cloud Strategy",
            "description": "Using the Ichimoku Cloud indicator to identify trend direction, support/resistance levels, and potential entry/exit points. When price is above the cloud, the trend is bullish; when price is below the cloud, the trend is bearish. The cloud itself represents support and resistance areas.",
            "author": "Alex Chen",
            "date": "2025-05-13T09:15:00Z",
            "likes": 29,
            "comments": 0
        }
    ]

if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'selected_strategy' not in st.session_state:
    st.session_state.selected_strategy = None

# Helper functions
def format_date(date_str):
    date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    return date.strftime("May %d, %Y")

# Display header
st.markdown('<div class="header-container"><div class="header-title">Knead Strategy Forum</div></div>', unsafe_allow_html=True)

# Search and button
col1, col2 = st.columns([4, 1])
with col1:
    search = st.text_input("Search strategies...", label_visibility="collapsed")
with col2:
    if st.button("New Strategy"):
        st.session_state.page = 'new'

# Display content
if st.session_state.page == 'home':
    # Filter strategies
    strategies = st.session_state.strategies
    if search:
        strategies = [s for s in strategies if search.lower() in s['title'].lower()]
    
    # Display strategies
    for strategy in strategies:
        st.markdown(f"""
        <div class="strategy-card">
            <div class="like-count">{strategy['likes']}</div>
            <div class="strategy-title">{strategy['title']}</div>
            <div class="strategy-author">by {strategy['author']}</div>
            <div class="strategy-description">{strategy['description']}</div>
            <div class="strategy-meta">
                <div>💬 {strategy['comments']} comments</div>
                <div>{format_date(strategy['date'])}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("View Details", key=f"view_{strategy['id']}"):
                st.session_state.page = 'detail'
                st.session_state.selected_strategy = strategy['id']
        with col2:
            if st.button("Like", key=f"like_{strategy['id']}"):
                # Simulate like action
                pass

elif st.session_state.page == 'detail':
    # Get selected strategy
    strategy = next((s for s in st.session_state.strategies if s['id'] == st.session_state.selected_strategy), None)
    
    if strategy:
        # Back button
        if st.button("← Back to Forum"):
            st.session_state.page = 'home'
            st.session_state.selected_strategy = None
        
        # Display strategy details
        st.markdown(f"""
        <div class="strategy-card">
            <div class="like-count">{strategy['likes']}</div>
            <div class="strategy-title">{strategy['title']}</div>
            <div class="strategy-author">by {strategy['author']}</div>
            <div class="strategy-description">{strategy['description']}</div>
            <div class="strategy-meta">
                <div>{format_date(strategy['date'])}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Like button
        if st.button("Like", key="detail_like"):
            # Simulate like action
            pass
        
        # Strategy metrics
        st.subheader("Strategy Metrics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Win Rate", "68%")
        with col2:
            st.metric("Risk-Reward", "1:2.5")
        with col3:
            st.metric("Max Drawdown", "12.4%")
        with col4:
            st.metric("Sharpe Ratio", "1.8")
        
        # Comments
        st.subheader("Comments")
        
        # Comment form
        with st.form("comment_form"):
            comment = st.text_area("Add a comment")
            submitted = st.form_submit_button("Post Comment")
            if submitted and comment:
                st.success("Comment added!")
        
        # Sample comments
        if strategy['comments'] > 0:
            st.markdown("""
            <div style="background-color: #f8f9fa; border-radius: 5px; padding: 10px; margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span style="color: #333; font-weight: bold;">Michael Brown</span>
                    <span style="color: #666; font-size: 12px;">May 18, 2025</span>
                </div>
                <p style="color: #333;">I've been testing this strategy for the past month and have seen consistent results. The key is to be patient and wait for clear signals rather than forcing trades.</p>
            </div>
            """, unsafe_allow_html=True)
            
            if strategy['comments'] > 1:
                st.markdown("""
                <div style="background-color: #f8f9fa; border-radius: 5px; padding: 10px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <span style="color: #333; font-weight: bold;">Alex Chen</span>
                        <span style="color: #666; font-size: 12px;">May 16, 2025</span>
                    </div>
                    <p style="color: #333;">Have you tried combining this with volume confirmation? I find it improves the reliability of the signals significantly.</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.error("Strategy not found")
        if st.button("Back to Forum"):
            st.session_state.page = 'home'
            st.session_state.selected_strategy = None

elif st.session_state.page == 'new':
    st.subheader("Create New Strategy")
    
    with st.form("new_strategy_form"):
        title = st.text_input("Title")
        description = st.text_area("Description", height=200)
        visibility = st.selectbox("Visibility", ["Public", "Private"])
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.form_submit_button("Cancel"):
                st.session_state.page = 'home'
        with col2:
            if st.form_submit_button("Post Strategy"):
                if title and description:
                    st.session_state.page = 'home'
                    st.success("Strategy posted!")
                else:
                    st.error("Please fill out all fields")
