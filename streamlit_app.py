import streamlit as st
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Knead Strategy Forum", layout="wide")

# Initial data definitions
initial_strategies = [
    {
        "id": 1,
        "title": "Moving Average Crossover Strategy",
        "author": "Sarah Johnson",
        "authorId": "sarah123",
        "description": (
            "This strategy identifies trend reversals by tracking when shorter-term moving averages "
            "cross above or below longer-term moving averages. When the 50-day MA crosses above the "
            "200-day MA, it generates a buy signal (golden cross). When it crosses below, it "
            "generates a sell signal (death cross)."
        ),
        "likes": 42,
        "liked": False,
        "date": "2025-05-17T14:30:00",
        "visibility": "public",
        "comments": [
            {"id": 1, "author": "Mark Wilson", "content": "I've been using a variant of this strategy with good results. Have you tried adjusting the timeframes?", "likes": 7, "liked": False},
            {"id": 2, "author": "Alex Chen",     "content": "What about adding volume confirmation to reduce false signals?", "likes": 3, "liked": False}
        ]
    },
    {
        "id": 2,
        "title": "RSI Divergence Trading",
        "author": "Michael Brown",
        "authorId": "mike_b",
        "description": (
            "This strategy focuses on identifying divergences between price action and RSI indicator. "
            "When price makes a higher high but RSI makes a lower high (bearish divergence), it suggests "
            "a potential reversal to the downside. Conversely, when price makes a lower low but RSI makes a "
            "higher low (bullish divergence), it suggests a potential reversal to the upside."
        ),
        "likes": 37,
        "liked": False,
        "date": "2025-05-15T09:15:00",
        "visibility": "public",
        "comments": [
            {"id": 1, "author": "Emma Davis",    "content": "I've had mixed results with this. What timeframe do you find works best?", "likes": 5, "liked": False},
            {"id": 2, "author": "Sarah Johnson","content": "Great strategy. I combine this with volume analysis for better results.", "likes": 8, "liked": False}
        ]
    },
    {
        "id": 3,
        "title": "Ichimoku Cloud Strategy",
        "author": "Alex Chen",
        "authorId": "alex_c",
        "description": (
            "Using the Ichimoku Cloud indicator to identify trend direction, support/resistance levels, "
            "and potential entry/exit points. When price is above the cloud, the trend is bullish; when below, bearish. "
            "Cloud crossovers and TK crosses serve as additional signals."
        ),
        "likes": 29,
        "liked": False,
        "date": "2025-05-12T16:45:00",
        "visibility": "public",
        "comments": []
    }
]

user_profiles = {
    "sarah123": {"name": "Sarah Johnson", "karma": 387, "strategies": 14, "following": False},
    "mike_b":     {"name": "Michael Brown", "karma": 256, "strategies": 8,  "following": True},
    "alex_c":     {"name": "Alex Chen",     "karma": 192, "strategies": 6,  "following": False},
    "emma_d":     {"name": "Emma Davis",    "karma": 145, "strategies": 4,  "following": False},
}

# Initialize session state
if 'strategies' not in st.session_state:
    st.session_state.strategies = initial_strategies.copy()
if 'user_profiles' not in st.session_state:
    st.session_state.user_profiles = user_profiles.copy()

if 'view' not in st.session_state:
    st.session_state.view = 'forum'
if 'selected_id' not in st.session_state:
    st.session_state.selected_id = None
if 'active_profile' not in st.session_state:
    st.session_state.active_profile = None
if 'search' not in st.session_state:
    st.session_state.search = ''
if 'new_strategy' not in st.session_state:
    st.session_state.new_strategy = {"title": "", "description": "", "visibility": "public"}
if 'new_comment' not in st.session_state:
    st.session_state.new_comment = ""

# Helper functions

def format_date(dt_str):
    dt = datetime.fromisoformat(dt_str)
    return dt.strftime("%b %d, %Y %I:%M %p")


def toggle_like_strategy(sid):
    for s in st.session_state.strategies:
        if s['id'] == sid:
            s['likes'] += -1 if s.get('liked', False) else 1
            s['liked'] = not s.get('liked', False)
            break


def toggle_like_comment(sid, cid):
    for s in st.session_state.strategies:
        if s['id'] == sid:
            for c in s['comments']:
                if c['id'] == cid:
                    c['likes'] += -1 if c.get('liked', False) else 1
                    c['liked'] = not c.get('liked', False)
                    return


def toggle_follow_user(uid):
    p = st.session_state.user_profiles.get(uid)
    if p:
        p['following'] = not p['following']

# Header with search and New Strategy
col1, col2 = st.columns([4, 1])
with col1:
    st.session_state.search = st.text_input("🔍 Search strategies...", value=st.session_state.search)
with col2:
    if st.session_state.view == 'forum' and st.button("New Strategy"):
        st.session_state.view = 'newStrategy'

st.markdown("---")

# Forum list view
if st.session_state.view == 'forum':
    filtered = [s for s in st.session_state.strategies
                if st.session_state.search.lower() in s['title'].lower() or st.session_state.search.lower() in s['author'].lower()]

    if not filtered:
        st.info("No strategies match your search.")
    for s in filtered:
        cols = st.columns([6, 1, 1, 1])
        with cols[0]:
            st.markdown(f"### {s['title']}")
            if st.button(f"by {s['author']}", key=f"author_{s['id']}"):
                st.session_state.active_profile = s['authorId']
            st.write(format_date(s['date']))
            st.write(s['description'])
        with cols[1]:
            if st.button(f"💬 {len(s['comments'])}", key=f"comments_{s['id']}"):
                st.session_state.selected_id = s['id']
                st.session_state.view = 'strategyDetail'
        with cols[2]:
            if st.button(f"💖 {s['likes']}", key=f"like_{s['id']}"):
                toggle_like_strategy(s['id'])
        with cols[3]:
            if st.button("View", key=f"view_{s['id']}"):
                st.session_state.selected_id = s['id']
                st.session_state.view = 'strategyDetail'

# New strategy form view
elif st.session_state.view == 'newStrategy':
    if st.button("← Back to Forum"):
        st.session_state.view = 'forum'
    st.header("Create New Strategy")
    ns = st.session_state.new_strategy
    ns['title'] = st.text_input("Title", ns['title'])
    ns['description'] = st.text_area("Description", ns['description'], height=200)
    ns['visibility'] = st.radio("Visibility", ['public', 'private'], index=0 if ns['visibility']=='public' else 1)
    if st.button("Post Strategy"):
        new_id = max([s['id'] for s in st.session_state.strategies]) + 1
        entry = {
            'id': new_id,
            'title': ns['title'],
            'author': 'You',
            'authorId': 'you',
            'description': ns['description'],
            'likes': 0,
            'liked': False,
            'date': datetime.utcnow().isoformat(),
            'visibility': ns['visibility'],
            'comments': []
        }
        st.session_state.strategies.insert(0, entry)
        st.success("Strategy posted!")
        st.session_state.new_strategy = {"title": "", "description": "", "visibility": "public"}
        st.session_state.view = 'forum'

# Detailed strategy + comments view
elif st.session_state.view == 'strategyDetail':
    strat = next((x for x in st.session_state.strategies if x['id'] == st.session_state.selected_id), None)
    if strat:
        if st.button("← Back to Forum"):
            st.session_state.view = 'forum'
        st.title(strat['title'])
        if st.button(f"by {strat['author']}", key="detail_author"):
            st.session_state.active_profile = strat['authorId']
        like_label = f"💖 {strat['likes']}"
        if st.button(like_label, key="detail_like"):
            toggle_like_strategy(strat['id'])
        st.write(format_date(strat['date']))
        st.write("---")
        st.write(strat['description'])
        st.subheader(f"Comments ({len(strat['comments'])})")

        # Existing comments
        for c in strat['comments']:
            ccols = st.columns([9, 1])
            with ccols[0]:
                st.markdown(f"**{c['author']}**: {c['content']}")
            with ccols[1]:
                if st.button(f"👍 {c['likes']}", key=f"clike_{strat['id']}_{c['id']}"):
                    toggle_like_comment(strat['id'], c['id'])
        # Add comment form
        with st.form(key='comment_form'):
            comment_input = st.text_area("Add a comment...", key='comment_input')
            submitted = st.form_submit_button("Post Comment")
            if submitted and comment_input.strip():
                new_c = {
                    'id': len(strat['comments']) + 1,
                    'author': 'You',
                    'content': comment_input,
                    'likes': 0,
                    'liked': False
                }
                strat['comments'].append(new_c)
                st.experimental_rerun()

# User profile sidebar
if st.session_state.active_profile:
    profile = st.session_state.user_profiles.get(st.session_state.active_profile)
    if profile:
        st.sidebar.header("User Profile")
        st.sidebar.write(f"**{profile['name']}**")
        st.sidebar.write(f"Karma Score: {profile['karma']}")
        st.sidebar.write(f"Strategies Posted: {profile['strategies']}")
        follow_label = "Unfollow" if profile['following'] else "Follow"
        if st.sidebar.button(follow_label):
            toggle_follow_user(st.session_state.active_profile)
        if st.sidebar.button("Close Profile"):
            st.session_state.active_profile = None
