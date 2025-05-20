import streamlit as st
import json
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Knead Strategy Forum",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for high contrast
st.markdown("""
<style>
/* Base Styles */
.main * {
    color: black !important;
}

.stButton button {
    background-color: #f0f2f6;
    border: 1px solid #aaa !important;
    color: black !important;
    font-weight: 500;
}

.stButton button:hover {
    border: 1px solid #666 !important;
    background-color: #e0e2e6;
}

.primary-btn {
    background-color: #1e88e5 !important;
    color: white !important;
    border: none !important;
    padding: 10px 15px;
    border-radius: 4px;
    font-weight: 500;
    text-align: center;
    cursor: pointer;
}

.card {
    background-color: white;
    border-radius: 8px;
    padding: 15px;
    margin-bottom: 15px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    border: 1px solid #ddd;
}

.strategy-title {
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 8px;
}

.strategy-meta {
    margin-bottom: 10px;
    font-size: 14px;
}

.strategy-description {
    margin-bottom: 15px;
}

.comment-card {
    background-color: #f8f9fa;
    border-radius: 6px;
    padding: 10px;
    margin-bottom: 10px;
    border: 1px solid #eee;
}

.metric-card {
    background-color: #f8f9fa;
    border-radius: 6px;
    padding: 10px;
    text-align: center;
    border: 1px solid #eee;
}

.metric-value {
    font-size: 24px;
    font-weight: 600;
}

.metric-label {
    font-size: 14px;
}

.reply-comment {
    margin-left: 30px;
    border-left: 2px solid #aaa;
    padding-left: 10px;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Initialize session state for data storage
if 'strategies' not in st.session_state:
    st.session_state.strategies = [
        {
            "id": "1",
            "title": "Mean Reversion Strategy for Forex",
            "description": "This strategy identifies overbought and oversold conditions in currency pairs. It uses Bollinger Bands and RSI indicators to identify potential reversal points. When price touches the upper Bollinger Band and RSI is above 70, it signals a sell opportunity. Conversely, when price touches the lower Bollinger Band and RSI is below 30, it signals a buy opportunity. The strategy includes proper position sizing (1% risk per trade) and implements a 2:1 reward-to-risk ratio for all trades with proper stop losses.",
            "author_id": "1",
            "author_name": "Alex Johnson",
            "date": "2025-05-15T10:30:00Z",
            "likes": 42,
            "liked": False,
            "visibility": "public"
        },
        {
            "id": "2",
            "title": "Trend Following Strategy with Moving Averages",
            "description": "This strategy focuses on capturing strong market trends using multiple moving averages. It uses a combination of 9 EMA, 21 EMA, and 50 SMA to identify trend direction and potential entry points. When the 9 EMA crosses above the 21 EMA and both are above the 50 SMA, it generates a buy signal. When the 9 EMA crosses below the 21 EMA and both are below the 50 SMA, it generates a sell signal. The strategy performs best in trending markets and includes trailing stops to maximize profits during strong trends.",
            "author_id": "2",
            "author_name": "Maya Rodriguez",
            "date": "2025-05-14T15:45:00Z",
            "likes": 38,
            "liked": False,
            "visibility": "public"
        },
        {
            "id": "3",
            "title": "Options Iron Condor for Low Volatility Markets",
            "description": "This options strategy capitalizes on low volatility environments using iron condors. By selling both an out-of-the-money call spread and an out-of-the-money put spread with the same expiration date, this strategy profits when the underlying asset stays within a specific price range. The ideal setup is during periods of low implied volatility and no expected major news events. Position sizing is critical, with maximum risk limited to 2% of account per trade.",
            "author_id": "3",
            "author_name": "Tao Chen",
            "date": "2025-05-13T09:15:00Z",
            "likes": 27,
            "liked": False,
            "visibility": "public"
        },
        {
            "id": "4",
            "title": "Volatility Breakout for Intraday Trading",
            "description": "This intraday strategy captures explosive price movements following tight consolidation periods. It waits for price to compress (measured by decreasing Average True Range) followed by a surge in volume and price movement outside the consolidation range. The strategy works best during the first 2 hours of market open or near significant news events. Entry is triggered when price breaks above/below the consolidation with volume confirmation, with tight stop losses placed just inside the consolidation range.",
            "author_id": "1",
            "author_name": "Alex Johnson",
            "date": "2025-05-12T14:20:00Z",
            "likes": 31,
            "liked": False,
            "visibility": "public"
        }
    ]

if 'comments' not in st.session_state:
    st.session_state.comments = [
        {
            "id": "101",
            "strategy_id": "1",
            "author_id": "2",
            "author_name": "Maya Rodriguez",
            "text": "I've been testing this strategy for the past month and have seen consistent results. The key is to be patient and wait for clear signals rather than forcing trades.",
            "date": "2025-05-16T08:30:00Z",
            "parent_id": None
        },
        {
            "id": "102",
            "strategy_id": "1",
            "author_id": "3",
            "author_name": "Tao Chen",
            "text": "Have you tried adjusting the RSI thresholds for different currency pairs? I've found that some pairs work better with custom settings.",
            "date": "2025-05-16T10:15:00Z",
            "parent_id": None
        },
        {
            "id": "103",
            "strategy_id": "1",
            "author_id": "1",
            "author_name": "Alex Johnson",
            "text": "Good point! For EUR/USD I use 75/25 thresholds instead of the standard 70/30.",
            "date": "2025-05-16T11:05:00Z",
            "parent_id": "102"
        }
    ]

if 'users' not in st.session_state:
    st.session_state.users = [
        {
            "id": "1",
            "name": "Alex Johnson",
            "karma": 387,
            "followed": False
        },
        {
            "id": "2",
            "name": "Maya Rodriguez",
            "karma": 259,
            "followed": False
        },
        {
            "id": "3",
            "name": "Tao Chen",
            "karma": 412,
            "followed": False
        }
    ]

if 'current_user' not in st.session_state:
    st.session_state.current_user = {
        "id": "1",
        "name": "Alex Johnson"
    }

# Initialize navigation state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'view_strategy_id' not in st.session_state:
    st.session_state.view_strategy_id = None
if 'view_author_id' not in st.session_state:
    st.session_state.view_author_id = None

# Utility Functions
def format_date(date_string):
    date_obj = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
    return date_obj.strftime("%b %d, %Y")

def get_preview(text, max_len=150):
    if len(text) > max_len:
        return text[:max_len] + "..."
    return text

def toggle_like(strategy_id):
    for s in st.session_state.strategies:
        if s["id"] == strategy_id:
            s["liked"] = not s["liked"]
            if s["liked"]:
                s["likes"] += 1
            else:
                s["likes"] -= 1
            break

def add_comment(strategy_id, text, parent_id=None):
    comment = {
        "id": str(1000 + len(st.session_state.comments)),
        "strategy_id": strategy_id,
        "author_id": st.session_state.current_user["id"],
        "author_name": st.session_state.current_user["name"],
        "text": text,
        "date": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "parent_id": parent_id
    }
    st.session_state.comments.append(comment)

def create_strategy(title, description, visibility):
    new_strategy = {
        "id": str(100 + len(st.session_state.strategies)),
        "title": title,
        "description": description,
        "author_id": st.session_state.current_user["id"],
        "author_name": st.session_state.current_user["name"],
        "date": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "likes": 0,
        "liked": False,
        "visibility": visibility
    }
    st.session_state.strategies.insert(0, new_strategy)

# Header and Navigation
st.header("Knead Strategy Forum")

col1, col2 = st.columns([7, 2])
with col2:
    col2a, col2b = st.columns(2)
    with col2a:
        if st.button("Home", key="nav_home"):
            st.session_state.page = 'home'
            st.session_state.view_strategy_id = None
            st.session_state.view_author_id = None
    with col2b:
        if st.button("New Strategy", key="nav_new"):
            st.session_state.page = 'new_strategy'
            st.session_state.view_strategy_id = None
            st.session_state.view_author_id = None

# Main Content
if st.session_state.page == 'home':
    # Search and filter 
    search_term = st.text_input("Search strategies...")
    
    # Author filter display
    if st.session_state.view_author_id:
        author = next((u for u in st.session_state.users if u["id"] == st.session_state.view_author_id), None)
        if author:
            st.info(f"Showing strategies by {author['name']}")
            if st.button("Clear Filter", key="clear_filter"):
                st.session_state.view_author_id = None
    
    # Filter strategies
    filtered_strategies = st.session_state.strategies.copy()
    
    # Apply author filter
    if st.session_state.view_author_id:
        filtered_strategies = [s for s in filtered_strategies if s["author_id"] == st.session_state.view_author_id]
    
    # Apply search filter
    if search_term:
        filtered_strategies = [s for s in filtered_strategies if search_term.lower() in s["title"].lower()]
    
    # Display strategies
    if not filtered_strategies:
        st.warning("No strategies found matching your criteria.")
    
    for idx, strategy in enumerate(filtered_strategies):
        st.markdown(f'<div class="card">', unsafe_allow_html=True)
        
        # Strategy title and meta
        st.markdown(f'<div class="strategy-title">{strategy["title"]}</div>', unsafe_allow_html=True)
        
        # Author and date
        auth_col, date_col = st.columns([1, 1])
        with auth_col:
            if st.button(f"By {strategy['author_name']}", key=f"author_{idx}"):
                st.session_state.view_author_id = strategy["author_id"]
        with date_col:
            st.markdown(f'<div style="text-align: right">{format_date(strategy["date"])}</div>', unsafe_allow_html=True)
        
        # Strategy description
        st.markdown(f'<div class="strategy-description">{get_preview(strategy["description"])}</div>', unsafe_allow_html=True)
        
        # Action buttons
        view_col, like_col, comment_col = st.columns([1, 1, 5])
        with view_col:
            if st.button("View Details", key=f"view_{idx}"):
                st.session_state.page = 'strategy_detail'
                st.session_state.view_strategy_id = strategy["id"]
        with like_col:
            like_text = "Unlike" if strategy["liked"] else "Like"
            if st.button(f"{like_text}", key=f"like_{idx}"):
                toggle_like(strategy["id"])
        with comment_col:
            comment_count = len([c for c in st.session_state.comments if c["strategy_id"] == strategy["id"]])
            st.markdown(f"<div style='text-align: right'>💬 {comment_count} comments</div>", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == 'strategy_detail':
    # Get strategy details
    strategy = next((s for s in st.session_state.strategies if s["id"] == st.session_state.view_strategy_id), None)
    
    if not strategy:
        st.error("Strategy not found")
        if st.button("Back to Home", key="back_home_error"):
            st.session_state.page = 'home'
    else:
        # Navigation
        if st.button("← Back to Forum", key="back_to_forum"):
            st.session_state.page = 'home'
        
        # Strategy details
        st.markdown(f'<div class="card">', unsafe_allow_html=True)
        st.markdown(f'<h2>{strategy["title"]}</h2>', unsafe_allow_html=True)
        
        auth_col, date_col = st.columns([1, 1])
        with auth_col:
            if st.button(f"Author: {strategy['author_name']}", key="detail_author"):
                st.session_state.page = 'home'
                st.session_state.view_author_id = strategy["author_id"]
        with date_col:
            st.markdown(f'<div style="text-align: right">{format_date(strategy["date"])}</div>', unsafe_allow_html=True)
        
        st.markdown(f'<div class="strategy-description">{strategy["description"]}</div>', unsafe_allow_html=True)
        
        # Like button
        like_text = "Unlike" if strategy["liked"] else "Like"
        if st.button(f"{like_text} ({strategy['likes']})", key="detail_like"):
            toggle_like(strategy["id"])
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Strategy metrics
        st.subheader("Strategy Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown('<div class="metric-value">68%</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Win Rate</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown('<div class="metric-value">1:2.5</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Risk-Reward</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown('<div class="metric-value">12.4%</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Max Drawdown</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown('<div class="metric-value">1.8</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Sharpe Ratio</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Comments section
        st.subheader("Comments")
        
        # Comment form
        with st.form("comment_form"):
            new_comment = st.text_area("Add a comment")
            submitted = st.form_submit_button("Post Comment")
            if submitted and new_comment:
                add_comment(strategy["id"], new_comment)
        
        # Display comments
        root_comments = [c for c in st.session_state.comments if c["strategy_id"] == strategy["id"] and c["parent_id"] is None]
        root_comments.sort(key=lambda x: x["date"], reverse=True)
        
        if not root_comments:
            st.info("No comments yet. Be the first to comment!")
        
        for idx, comment in enumerate(root_comments):
            st.markdown(f'<div class="comment-card">', unsafe_allow_html=True)
            
            auth_col, date_col = st.columns([1, 1])
            with auth_col:
                if st.button(comment["author_name"], key=f"comment_author_{idx}"):
                    st.session_state.page = 'home'
                    st.session_state.view_author_id = comment["author_id"]
            with date_col:
                st.markdown(f'<div style="text-align: right">{format_date(comment["date"])}</div>', unsafe_allow_html=True)
            
            st.markdown(f"<p>{comment['text']}</p>", unsafe_allow_html=True)
            
            # Show replies
            replies = [c for c in st.session_state.comments if c["parent_id"] == comment["id"]]
            for reply_idx, reply in enumerate(replies):
                st.markdown(f'<div class="reply-comment">', unsafe_allow_html=True)
                
                reply_auth_col, reply_date_col = st.columns([1, 1])
                with reply_auth_col:
                    if st.button(reply["author_name"], key=f"reply_author_{idx}_{reply_idx}"):
                        st.session_state.page = 'home'
                        st.session_state.view_author_id = reply["author_id"]
                with reply_date_col:
                    st.markdown(f'<div style="text-align: right">{format_date(reply["date"])}</div>', unsafe_allow_html=True)
                
                st.markdown(f"<p>{reply['text']}</p>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == 'new_strategy':
    st.subheader("Create New Strategy")
    
    with st.form("new_strategy_form"):
        title = st.text_input("Title")
        description = st.text_area("Description", height=200)
        visibility = st.selectbox("Visibility", ["public", "private"])
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.form_submit_button("Cancel"):
                st.session_state.page = 'home'
        with col2:
            if st.form_submit_button("Post Strategy"):
                if not title:
                    st.error("Title is required")
                elif not description:
                    st.error("Description is required")
                else:
                    create_strategy(title, description, visibility)
                    st.session_state.page = 'home'
