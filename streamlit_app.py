import streamlit as st
import os
import subprocess
import time
from pathlib import Path

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

def setup_frontend():
    """Check if frontend is set up, if not, set it up"""
    frontend_dir = Path("frontend")
    
    if not frontend_dir.exists():
        st.info("Setting up the frontend for the first time. This may take a few minutes...")
        
        # Create the frontend directory
        frontend_dir.mkdir(exist_ok=True)
        
        # Create React app
        subprocess.run(["npx", "create-react-app", "frontend"], check=True)
        
        # Install dependencies
        subprocess.run(["npm", "install", "react-router-dom", "react-icons"], 
                      cwd="frontend", check=True)
        
        # Copy our files to the frontend directory
        # This would happen in a real deployment

        # Build the app
        subprocess.run(["npm", "run", "build"], cwd="frontend", check=True)
        
        st.success("Frontend setup complete!")
        st.experimental_rerun()

def main():
    # Setup check
    if not Path("frontend/build").exists():
        setup_frontend()
        return
    
    st.title("Knead Strategy Forum")
    
    # Embed the React app
    if Path("frontend/build/index.html").exists():
        # In production, we'd serve the built React app
        with open("frontend/build/index.html", "r") as f:
            html_content = f.read()
        
        st.components.v1.html(html_content, height=800, scrolling=True)
    else:
        st.error("React app not built. Please run 'npm run build' in the frontend directory.")

if __name__ == "__main__":
    main()
