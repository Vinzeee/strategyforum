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

# Custom CSS for purple color scheme
st.markdown("""
<style>
/* Base Styles */
body {
    font-family: 'Segoe UI', 'Roboto', 'Oxygen', sans-serif;
    color: #333;
    background-color: #f8f9fa;
}

/* Header */
.header {
    background-color: #5E35B1;
    color: white;
    padding: 1rem;
    margin-bottom: 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.header h1 {
    color: white !important;
    margin: 0;
    font-weight: 600;
}

/* Strategy Card */
.strategy-card {
    background-color: white;
    border-radius: 10px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    border: 1px solid #f0f0f0;
}

.strategy-title {
    font-size: 22px;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: #333;
}

.author-line {
    font-size: 14px;
    color: #666;
    margin-bottom: 1rem;
}

.strategy-description {
    color: #444;
    margin-bottom: 1rem;
    line-height: 1.6;
}

.card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 0.5rem;
}

.comments-count {
    display: flex;
    align-items: center;
    color: #666;
    font-size: 14px;
}

.date {
    color: #666;
    font-size: 14px;
}

/* Likes */
.likes {
    color: #666;
    font-size: 18px;
    display: flex;
    align-items: center;
}

.likes svg {
    margin-right: 0.25rem;
}

/* Comments */
.comment-card {
    background-color: #f9f9fb;
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 0.75rem;
    border: 1px solid #eee;
}

.comment-author {
    font-weight: 600;
    color: #333;
}

.comment-date {
    font-size: 12px;
    color: #777;
}

.comment-content {
    margin-top: 0.5rem;
    color: #333;
}

.reply-comment {
    margin-left: 2rem;
    margin-top: 0.75rem;
    padding-left: 1rem;
    border-left: 2px solid #ddd;
}

/* Form elements */
.btn-primary {
    background-color: #5E35B1 !important;
    color: white !important;
    border: none !important;
    padding: 0.5rem 1rem;
    border-radius: 5px;
    cursor: pointer;
    font-weight: 500;
}

.stButton button {
    border-radius: 5px !important;
}

.strategy-metrics {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 16px;
    margin: 1.5rem 0;
}

.metric-card {
    background-color: #f8f9fa;
    border-radius: 8px;
    padding: 1rem;
    text-align: center;
    border: 1px solid #eee;
}

.metric-value {
    font-size: 24px;
    font-weight: 600;
    color: #5E35B1;
}

.metric-label {
    font-size: 14px;
    color: #666;
}

/* Remove Streamlit styling */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stButton {
    margin-bottom: 0 !important;
}

/* Custom search box */
.search-container {
    display: flex;
    align-items: center;
    max-width: 600px;
    margin-bottom: 2rem;
    border-radius: 50px;
    background-color: white;
    padding: 0.25rem 1rem;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.search-container input {
    flex: 1;
    border: none;
    padding: 0.5rem;
    font-size: 16px;
    background: transparent;
}

.search-container input:focus {
    outline: none;
}

/* New Strategy Button */
.new-strategy-btn {
    background-color: white;
    color: #5E35B1 !important;
    border: 1px solid #5E35B1 !important;
    padding: 0.5rem 1.25rem;
    border-radius: 50px;
    font-weight: 500;
    cursor: pointer;
    text-align: center;
}

/* Override for dark text */
.strategy-title, .strategy-description, .comment-content, h1, h2, h3, p {
    color: #333 !important;
}

/* Like button */
.like-area {
    display: flex;
    align-items: center;
    position: absolute;
    top: 20px;
    right: 20px;
}

.like-count {
    margin-left: 8px;
    font-size: 18px;
    color: #666;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state for data storage
if 'strategies' not in st.session_state:
    st.session_state.strategies = [
        {
            "id": "1",
            "title": "Moving Average Crossover Strategy",
            "description": "This strategy identifies trend reversals by tracking when shorter-term moving averages cross above or below longer-term moving averages. When the 50-day moving average crosses above the 200-day moving average (golden cross), it generates a buy signal. When the 50-day moving average crosses below the 200-day moving average (death cross), it generates a sell signal. The strategy works best in trending markets and filters out market noise.",
            "author_id": "1",
            "author_name": "Sarah Johnson",
            "date": "2025-05-17T10:30:00Z",
            "likes": 42,
            "liked": False,
            "comments": 2,
            "visibility": "public"
        },
        {
            "id": "2",
            "title": "RSI Divergence Trading",
            "description": "This strategy focuses on identifying divergences between price action and RSI indicator. When price makes a higher high but RSI makes a lower high (bearish divergence), it signals a potential trend reversal to the downside. Conversely, when price makes a lower low but RSI makes a higher low (bullish divergence), it signals a potential trend reversal to the upside. RSI divergence is especially effective for finding market turning points.",
            "author_id": "2",
            "author_name": "Michael Brown",
            "date": "2025-05-15T15:45:00Z",
            "likes": 37,
            "liked": False,
            "comments": 2,
            "visibility": "public"
        },
        {
            "id": "3",
            "title": "Ichimoku Cloud Strategy",
            "description": "Using the Ichimoku Cloud indicator to identify trend direction, support/resistance levels, and potential entry/exit points. When price is above the cloud, the trend is bullish; when price is below the cloud, the trend is bearish. The cloud itself represents support and resistance areas. The strategy also uses Tenkan-sen and Kijun-sen lines for signals and the Chikou Span for confirmation.",
            "author_id": "3",
            "author_name": "Alex Chen",
            "date": "2025-05-13T09:15:00Z",
            "likes": 29,
            "liked": False,
            "comments": 0,
            "visibility": "public"
        },
        {
            "id": "4",
            "title": "Bollinger Band Squeeze Strategy",
            "description": "This strategy identifies periods of low volatility followed by volatility expansion. When Bollinger Bands tighten (the squeeze), it suggests a period of consolidation before a strong price movement. The strategy waits for a breakout from the squeeze, confirmed by an increase in volume. The direction of the breakout determines the trade direction. It's effective across multiple timeframes and markets.",
            "author_id": "1",
            "author_name": "Sarah Johnson",
            "date": "2025-05-10T14:20:00Z",
            "likes": 31,
            "liked": False,
            "comments": 4,
            "visibility": "public"
        }
    ]

if 'comments' not in st.session_state:
    st.session_state.comments = [
        {
            "id": "101",
            "strategy_id": "1",
            "author_id": "2",
            "author_name": "Michael Brown",
            "text": "I've been testing this strategy for the past month and have seen consistent results. The key is to be patient and wait for clear signals rather than forcing trades.",
            "date": "2025-05-18T08:30:00Z",
            "parent_id": None
        },
        {
            "id": "102",
            "strategy_id": "1",
            "author_id": "3",
            "author_name": "Alex Chen",
            "text": "Have you tried combining this with volume confirmation? I find it improves the reliability of the signals significantly.",
            "date": "2025-05-18T10:15:00Z",
            "parent_id": None
        },
        {
            "id": "103",
            "strategy_id": "2",
            "author_id": "1",
            "author_name": "Sarah Johnson",
            "text": "Great strategy. I've found adding a trend filter makes this even more effective, only taking divergence trades in the direction of the larger trend.",
            "date": "2025-05-16T11:05:00Z",
            "parent_id": None
        },
        {
            "id": "104",
            "strategy_id": "2",
            "author_id": "3",
            "author_name": "Alex Chen",
            "text": "What timeframe do you find works best for RSI divergence? I've had more success on the 4h and daily charts than on shorter timeframes.",
            "date": "2025-05-16T13:22:00Z",
            "parent_id": None
        }
    ]

if 'users' not in st.session_state:
    st.session_state.users = [
        {
            "id": "1",
            "name": "Sarah Johnson",
            "karma": 387,
            "followed": False
        },
        {
            "id": "2",
            "name": "Michael Brown",
            "karma": 259,
            "followed": False
        },
        {
            "id": "3",
            "name": "Alex Chen",
            "karma": 412,
            "followed": False
        }
    ]

if 'current_user' not in st.session_state:
    st.session_state.current_user = {
        "id": "1",
        "name": "Sarah Johnson"
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
        "comments": 0,
        "visibility": visibility
    }
    st.session_state.strategies.insert(0, new_strategy)

# Custom header with purple background
st.markdown("""
<div class="header">
    <h1>Knead Strategy Forum</h1>
</div>
""", unsafe_allow_html=True)

# Navigation for home or strategy creation
col1, col2 = st.columns([3, 1])
with col1:
    search_term = st.text_input("Search strategies...", placeholder="Search strategies...")
with col2:
    if st.button("New Strategy", key="new_strategy_btn"):
        st.session_state.page = 'new_strategy'

# Main Content
if st.session_state.page == 'home':
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
        # Card with title and author on left, likes on right
        st.markdown(f'''
        <div class="strategy-card" style="position: relative;">
            <div class="like-area">
                <span class="like-count">{strategy["likes"]}</span>
            </div>
            <h2 class="strategy-title">{strategy["title"]}</h2>
            <div class="author-line">by {strategy["author_name"]}</div>
            <div class="strategy-description">{get_preview(strategy["description"])}</div>
            <div class="card-footer">
                <div class="comments-count">
                    <span>💬 {strategy["comments"]} comments</span>
                </div>
                <div class="date">
                    {format_date(strategy["date"])}
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("View Details", key=f"view_{idx}"):
                st.session_state.page = 'strategy_detail'
                st.session_state.view_strategy_id = strategy["id"]
        with col2:
            like_text = "Unlike" if strategy["liked"] else "Like"
            if st.button(like_text, key=f"like_{idx}"):
                toggle_like(strategy["id"])

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
        st.markdown(f'''
        <div class="strategy-card" style="position: relative;">
            <div class="like-area">
                <span class="like-count">{strategy["likes"]}</span>
            </div>
            <h2 class="strategy-title">{strategy["title"]}</h2>
            <div class="author-line">by {strategy["author_name"]}</div>
            <div class="strategy-description">{strategy["description"]}</div>
            <div class="card-footer">
                <div class="date">
                    {format_date(strategy["date"])}
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Like button
        like_text = "Unlike" if strategy["liked"] else "Like"
        if st.button(f"{like_text}", key="detail_like"):
            toggle_like(strategy["id"])
        
        # Strategy metrics
        st.subheader("Strategy Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown('''
            <div class="metric-card">
                <div class="metric-value">68%</div>
                <div class="metric-label">Win Rate</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown('''
            <div class="metric-card">
                <div class="metric-value">1:2.5</div>
                <div class="metric-label">Risk-Reward</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            st.markdown('''
            <div class="metric-card">
                <div class="metric-value">12.4%</div>
                <div class="metric-label">Max Drawdown</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col4:
            st.markdown('''
            <div class="metric-card">
                <div class="metric-value">1.8</div>
                <div class="metric-label">Sharpe Ratio</div>
            </div>
            ''', unsafe_allow_html=True)
        
        # Comments section
        st.subheader("Comments")
        
        # Comment form
        with st.form("comment_form"):
            new_comment = st.text_area("Add a comment")
            submitted = st.form_submit_button("Post Comment")
            if submitted and new_comment:
                add_comment(strategy["id"], new_comment)
                for s in st.session_state.strategies:
                    if s["id"] == strategy["id"]:
                        s["comments"] += 1
        
        # Display comments
        strategy_comments = [c for c in st.session_state.comments if c["strategy_id"] == strategy["id"] and c["parent_id"] is None]
        strategy_comments.sort(key=lambda x: x["date"], reverse=True)
        
        if not strategy_comments:
            st.info("No comments yet. Be the first to comment!")
        
        for idx, comment in enumerate(strategy_comments):
            st.markdown(f'''
            <div class="comment-card">
                <div style="display: flex; justify-content: space-between;">
                    <span class="comment-author">{comment["author_name"]}</span>
                    <span class="comment-date">{format_date(comment["date"])}</span>
                </div>
                <div class="comment-content">{comment["text"]}</div>
            </div>
            ''', unsafe_allow_html=True)
            
            # Author button
            if st.button(f"View posts by {comment['author_name']}", key=f"comment_author_{idx}"):
                st.session_state.page = 'home'
                st.session_state.view_author_id = comment["author_id"]
            
            # Show replies
            replies = [c for c in st.session_state.comments if c["parent_id"] == comment["id"]]
            for reply_idx, reply in enumerate(replies):
                st.markdown(f'''
                <div class="reply-comment">
                    <div style="display: flex; justify-content: space-between;">
                        <span class="comment-author">{reply["author_name"]}</span>
                        <span class="comment-date">{format_date(reply["date"])}</span>
                    </div>
                    <div class="comment-content">{reply["text"]}</div>
                </div>
                ''', unsafe_allow_html=True)
                
                # Author button for reply
                if st.button(f"View posts by {reply['author_name']}", key=f"reply_author_{idx}_{reply_idx}"):
                    st.session_state.page = 'home'
                    st.session_state.view_author_id = reply["author_id"]

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
