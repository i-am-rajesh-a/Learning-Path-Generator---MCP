import streamlit as st
from utils import run_agent_sync
import os
from dotenv import load_dotenv

st.set_page_config(page_title="MCP POC", page_icon="🤖", layout="wide")

# Load environment variables from .env file
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
YOUTUBE_PIPEDREAM_URL = os.getenv("YOUTUBE_PIPEDREAM_URL")
DRIVE_PIPEDREAM_URL = os.getenv("DRIVE_PIPEDREAM_URL")
NOTION_PIPEDREAM_URL = os.getenv("NOTION_PIPEDREAM_URL")

st.title("Model Context Protocol(MCP) - Learning Path Generator")

# Initialize session state for progress
if 'current_step' not in st.session_state:
    st.session_state.current_step = ""
if 'progress' not in st.session_state:
    st.session_state.progress = 0
if 'last_section' not in st.session_state:
    st.session_state.last_section = ""
if 'is_generating' not in st.session_state:
    st.session_state.is_generating = False

# Sidebar for API and URL configuration
st.sidebar.header("Configuration")

# Remove API Key and Pipedream URL inputs from sidebar
# (No user input for API keys or URLs)

# Secondary tool selection (optional, for display only)
secondary_tool = st.sidebar.radio(
    "Select Secondary Tool:",
    ["Drive", "Notion"]
)

# Quick guide before goal input
st.info("""
**Quick Guide:**
1. Select your secondary tool (Drive or Notion)
2. Enter a clear learning goal, for example:
    - "I want to learn python basics in 3 days"
    - "I want to learn data science basics in 10 days"
""")

# Main content area
st.header("Enter Your Goal")
user_goal = st.text_input("Enter your learning goal:",
                        help="Describe what you want to learn, and we'll generate a structured path using YouTube content and your selected tool.")

# Progress area
progress_container = st.container()
progress_bar = st.empty()

def update_progress(message: str):
    """Update progress in the Streamlit UI"""
    st.session_state.current_step = message
    
    # Determine section and update progress
    if "Setting up agent with tools" in message:
        section = "Setup"
        st.session_state.progress = 0.1
    elif "Added Google Drive integration" in message or "Added Notion integration" in message:
        section = "Integration"
        st.session_state.progress = 0.2
    elif "Creating AI agent" in message:
        section = "Setup"
        st.session_state.progress = 0.3
    elif "Generating your learning path" in message:
        section = "Generation"
        st.session_state.progress = 0.5
    elif "Learning path generation complete" in message:
        section = "Complete"
        st.session_state.progress = 1.0
        st.session_state.is_generating = False
    else:
        section = st.session_state.last_section or "Progress"
    
    st.session_state.last_section = section
    
    # Show progress bar
    progress_bar.progress(st.session_state.progress)
    
    # Update progress container with current status
    with progress_container:
        # Show section header if it changed
        if section != st.session_state.last_section and section != "Complete":
            st.write(f"**{section}**")
        
        # Show message with tick for completed steps
        if message == "Learning path generation complete!":
            st.success("All steps completed! 🎉")
        else:
            prefix = "✓" if st.session_state.progress >= 0.5 else "→"
            st.write(f"{prefix} {message}")

# Generate Learning Path button
if st.button("Generate Learning Path", type="primary", disabled=st.session_state.is_generating):
    if not GOOGLE_API_KEY:
        st.error("Google API key not found. Please check your .env file.")
    elif not YOUTUBE_PIPEDREAM_URL:
        st.error("YouTube Pipedream URL not found. Please check your .env file.")
    elif (secondary_tool == "Drive" and not DRIVE_PIPEDREAM_URL) or (secondary_tool == "Notion" and not NOTION_PIPEDREAM_URL):
        st.error(f"Pipedream {secondary_tool} URL not found. Please check your .env file.")
    elif not user_goal:
        st.warning("Please enter your learning goal.")
    else:
        try:
            # Set generating flag
            st.session_state.is_generating = True
            # Reset progress
            st.session_state.current_step = ""
            st.session_state.progress = 0
            st.session_state.last_section = ""
            result = run_agent_sync(
                google_api_key=GOOGLE_API_KEY,
                youtube_pipedream_url=YOUTUBE_PIPEDREAM_URL,
                drive_pipedream_url=DRIVE_PIPEDREAM_URL,
                notion_pipedream_url=NOTION_PIPEDREAM_URL,
                user_goal=user_goal,
                progress_callback=update_progress
            )
            # Display results
            st.header("Your Learning Path")
            if result and "messages" in result:
                for msg in result["messages"]:
                    st.markdown(f"📚 {msg.content}")
            else:
                st.error("No results were generated. Please try again.")
                st.session_state.is_generating = False
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.error("Please check your .env file and try again.")
            st.session_state.is_generating = False
