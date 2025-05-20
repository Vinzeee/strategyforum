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

# Hide Streamlit branding
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Custom CSS for styling
st.markdown("""
<style>
/* Base Styles */
body {
    font-family: 'Segoe UI', 'Roboto', 'Oxygen', sans-serif;
    color: #333;
    background-color: #f5f7fa;
}

/* Card Style */
.strategy-card {
    background-color: white;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.strategy-title {
    font-size: 22px;
    font-weight: 600;
    margin-bottom: 10px;
}

.strategy-meta {
    display: flex;
    justify-content: space-between;
    font-size: 14px;
    color: #666;
    margin-bottom: 15px;
}

.strategy-description {
    margin-bottom: 20px;
    line-height: 1.6;
}

.strategy-actions {
    display: flex;
    align-items: center;
}

.likes {
    display: flex;
    align-items: center;
    margin-right: 20px;
}

.btn-primary {
    background-color: #1e88e5;
    color: white;
    padding: 8px 16px;
    border-radius: 4px;
    text-decoration: none;
    border: none;
    cursor: pointer;
}

.btn-primary:hover {
    background-color: #1976d2;
}

/* Form styles */
.form-group {
    margin-bottom: 20px;
}

label {
    display: block;
    margin-bottom: 8px;
    font-weight: 500;
}

textarea, select {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

.error {
    color: #ff4757;
    font-size: 14px;
    margin-top: 4px;
}

/* Strategy detail */
.strategy-header {
    margin-bottom: 24px;
    padding-bottom: 16px;
    border-bottom: 1px solid #eee;
}

.metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 16px;
    margin-bottom: 30px;
}

.metric {
    background-color: #f5f7fa;
    border-radius: 6px;
    padding: 16px;
}

.metric-label {
    font-size: 14px;
    color: #666;
    margin-bottom: 4px;
}

.metric-value {
    font-size: 24px;
    font-weight: 600;
}

/* Comment styles */
.comment-item {
    background-color: #f9f9f9;
    border-radius: 6px;
    padding: 15px;
    margin-bottom: 10px;
}

.comment-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 8px;
}

.comment-author {
    font-weight: 500;
    color: #1e88e5;
}

.comment-content {
    margin-bottom: 5px;
}

.comment-replies {
    margin-left: 30px;
    padding-left: 10px;
    border-left: 2px solid #e0e0e0;
}
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

# Format date
def format_date(date_string):
    date_obj = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
    return date_obj.strftime("%b %d, %Y")

# Get preview of description
def get_description_preview(description, max_length=150):
    if len(description) > max_length:
        return description[:max_length] + "..."
    return description

# Toggle like on a strategy
def toggle_like(strategy_id):
    for strategy in st.session_state.strategies:
        if strategy["id"] == strategy_id:
            strategy["liked"] = not strategy["liked"]
            if strategy["liked"]:
                strategy["likes"] += 1
            else:
                strategy["likes"] -= 1
            break

# Add a comment
def add_comment(strategy_id, text, parent_id=None):
    new_comment = {
        "id": str(len(st.session_state.comments) + 1000),
        "strategy_id": strategy_id,
        "author_id": st.session_state.current_user["id"],
        "author_name": st.session_state.current_user["name"],
        "text": text,
        "date": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "parent_id": parent_id
    }
    st.session_state.comments.append(new_comment)

# Add a new strategy
def add_strategy(title, description, visibility):
    new_strategy = {
        "id": str(len(st.session_state.strategies) + 100),
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

# Navigation
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'selected_strategy' not in st.session_state:
    st.session_state.selected_strategy = None
if 'selected_author' not in st.session_state:
    st.session_state.selected_author = None

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.title("Knead Strategy Forum")
with col2:
    st.button("Home", key="home_btn", on_click=lambda: setattr(st.session_state, 'page', 'home'))
    st.button("New Strategy", key="new_btn", on_click=lambda: setattr(st.session_state, 'page', 'new'))

# Main content
if st.session_state.page == 'home':
    # Strategy Forum Home Page
    search = st.text_input("Search strategies...", key="search")
    
    # Author filter display
    if st.session_state.selected_author:
        author_name = next((user["name"] for user in st.session_state.users if user["id"] == st.session_state.selected_author), "Unknown")
        st.info(f"Showing strategies by {author_name}")
        if st.button("Clear Filter"):
            st.session_state.selected_author = None
            st.experimental_rerun()
    
    # Filter strategies
    filtered_strategies = []
    for strategy in st.session_state.strategies:
        if st.session_state.selected_author and strategy["author_id"] != st.session_state.selected_author:
            continue
        if search and search.lower() not in strategy["title"].lower():
            continue
        filtered_strategies.append(strategy)
    
    if not filtered_strategies:
        st.warning("No strategies found. Try adjusting your filters.")
    
    # Display strategies
    for strategy in filtered_strategies:
        with st.container():
            st.markdown(f"""
            <div class="strategy-card">
                <div class="strategy-title">{strategy["title"]}</div>
                <div class="strategy-meta">
                    <div>By <a href="#" onclick="return false;">{strategy["author_name"]}</a></div>
                    <div>{format_date(strategy["date"])}</div>
                </div>
                <div class="strategy-description">
                    {get_description_preview(strategy["description"])}
                </div>
                <div class="strategy-actions">
                    <div class="likes">
                        ❤️ {strategy["likes"]}
                    </div>
                    <div>
                        💬 {len([c for c in st.session_state.comments if c["strategy_id"] == strategy["id"]])}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button(f"View Details", key=f"view_{strategy['id']}"):
                    st.session_state.selected_strategy = strategy["id"]
                    st.session_state.page = 'detail'
                    st.experimental_rerun()
            with col2:
                like_text = "Unlike" if strategy["liked"] else "Like"
                if st.button(like_text, key=f"like_{strategy['id']}"):
                    toggle_like(strategy["id"])
                    st.experimental_rerun()

elif st.session_state.page == 'new':
    # New Strategy Form
    st.header("Create New Strategy")
    
    with st.form("new_strategy_form"):
        title = st.text_input("Title", key="title_input")
        description = st.text_area("Description", height=200, key="desc_input")
        visibility = st.selectbox("Visibility", ["public", "private"], key="visibility_input")
        
        submitted = st.form_submit_button("Post Strategy")
        if submitted:
            if not title:
                st.error("Title is required")
            elif not description:
                st.error("Description is required")
            else:
                add_strategy(title, description, visibility)
                st.session_state.page = 'home'
                st.experimental_rerun()
    
    if st.button("Cancel"):
        st.session_state.page = 'home'
        st.experimental_rerun()

elif st.session_state.page == 'detail':
    # Strategy Detail Page
    if st.session_state.selected_strategy:
        strategy = next((s for s in st.session_state.strategies if s["id"] == st.session_state.selected_strategy), None)
        
        if strategy:
            # Back button
            if st.button("← Back to Forum"):
                st.session_state.page = 'home'
                st.experimental_rerun()
            
            st.header(strategy["title"])
            
            # Strategy metadata
            st.markdown(f"""
            <div class="strategy-meta">
                <div>By <a href="#" onclick="return false;">{strategy["author_name"]}</a></div>
                <div>{format_date(strategy["date"])}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Strategy content
            st.markdown(f"<div class='strategy-description'>{strategy['description']}</div>", unsafe_allow_html=True)
            
            # Like button
            like_text = "Unlike" if strategy["liked"] else "Like"
            if st.button(f"{like_text} ({strategy['likes']})", key=f"detail_like"):
                toggle_like(strategy["id"])
                st.experimental_rerun()
            
            # Strategy metrics
            st.subheader("Strategy Metrics")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown("""
                <div class="metric">
                    <div class="metric-label">Win Rate</div>
                    <div class="metric-value">68%</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="metric">
                    <div class="metric-label">Risk-Reward</div>
                    <div class="metric-value">1:2.5</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div class="metric">
                    <div class="metric-label">Max Drawdown</div>
                    <div class="metric-value">12.4%</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown("""
                <div class="metric">
                    <div class="metric-label">Sharpe Ratio</div>
                    <div class="metric-value">1.8</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Comments section
            st.subheader("Comments")
            
            # Add comment form
            with st.form("add_comment_form"):
                comment_text = st.text_area("Add a comment", key="comment_input", height=100)
                comment_submitted = st.form_submit_button("Post Comment")
                
                if comment_submitted and comment_text:
                    add_comment(strategy["id"], comment_text)
                    st.experimental_rerun()
            
            # Display comments
            comments = [c for c in st.session_state.comments if c["strategy_id"] == strategy["id"] and c["parent_id"] is None]
            comments.sort(key=lambda x: x["date"], reverse=True)
            
            if not comments:
                st.info("No comments yet. Be the first to comment!")
            
            def render_comment(comment, level=0):
                st.markdown(f"""
                <div class="comment-item" style="margin-left: {level * 20}px;">
                    <div class="comment-header">
                        <span class="comment-author">{comment["author_name"]}</span>
                        <span>{format_date(comment["date"])}</span>
                    </div>
                    <div class="comment-content">{comment["text"]}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Look for replies
                replies = [c for c in st.session_state.comments if c["parent_id"] == comment["id"]]
                for reply in replies:
                    render_comment(reply, level + 1)
            
            for comment in comments:
                render_comment(comment)
        else:
            st.error("Strategy not found")
            if st.button("Back to Forum"):
                st.session_state.page = 'home'
                st.experimental_rerun()
