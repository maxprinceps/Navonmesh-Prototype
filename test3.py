import streamlit as st
import requests
from pathlib import Path
import speech_recognition as sr
import time
from threading import Thread
import queue
import json
from datetime import datetime

st.set_page_config(page_title="Nyyai Astra - Legal AI", layout="wide", initial_sidebar_state="collapsed")

# Initialize session state for voice recording
if 'voice_recording' not in st.session_state:
    st.session_state.voice_recording = False
if 'voice_text' not in st.session_state:
    st.session_state.voice_text = ""


# Initialize session states
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'search_history' not in st.session_state:
    st.session_state.search_history = []
if 'bookmarks' not in st.session_state:
    st.session_state.bookmarks = []
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []

def query_indian_kanoon(search_query):
    # Placeholder function for API integration (modify when you get API access)
    return f"Results for: {search_query}\n\n(Sample response from Indian Kanoon)"

def handle_login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        # Add your login logic here
        st.session_state.is_logged_in = True
        st.session_state.username = username
        st.rerun()

def handle_signup():
    st.subheader("Sign Up")
    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    if st.button("Sign Up"):
        if new_password == confirm_password:
            # Add your signup logic here
            st.success("Account created successfully! Please login.")
        else:
            st.error("Passwords don't match!")

def show_profile_modal():
    if not st.session_state.get('is_logged_in', False):
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        with tab1:
            handle_login()
        with tab2:
            handle_signup()
    else:
        st.subheader(f"Welcome, {st.session_state.username}!")
        if st.button("Logout"):
            st.session_state.is_logged_in = False
            st.session_state.username = None
            st.rerun()

def handle_file_upload():
    st.subheader("Upload Legal Documents")
    uploaded_files = st.file_uploader(
        "Choose your files", 
        accept_multiple_files=True,
        type=['pdf', 'docx', 'txt']
    )
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Create uploads directory if it doesn't exist
            Path("uploads").mkdir(exist_ok=True)
            
            # Save the file
            bytes_data = uploaded_file.read()
            file_path = f"uploads/{uploaded_file.name}"
            with open(file_path, "wb") as f:
                f.write(bytes_data)
            
            st.success(f"File '{uploaded_file.name}' uploaded successfully!")
            
            # Display file info
            file_stats = {
                "Filename": uploaded_file.name,
                "File type": uploaded_file.type,
                "File size": f"{round(len(bytes_data)/1024, 2)} KB"
            }
            
            st.json(file_stats)

def listen_for_speech(result_queue):
    """Background thread function for voice recognition"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            result_queue.put(("success", text))
        except sr.UnknownValueError:
            result_queue.put(("error", "Could not understand audio"))
        except sr.RequestError:
            result_queue.put(("error", "Could not request results from speech recognition service"))

def show_voice_search_modal():
    """Modal for voice search with better UI"""
    st.subheader("Voice Search 🎤")
    
    col1, col2 = st.columns([3,1])
    
    with col1:
        st.markdown("""
            <div style="padding: 20px; border-radius: 10px; background-color: #0000;">
                <p> Speak your legal query 🎙️...</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Show recognized text
        if st.session_state.voice_text:
            st.text_area("Recognized Text:", st.session_state.voice_text, height=100)
            # Add a button to use the recognized text
            if st.button("Use this text"):
                # Store the text in a temporary session state variable
                st.session_state.temp_search_text = st.session_state.voice_text
                st.session_state.show_voice_modal = False
                st.rerun()
    
    with col2:
        if not st.session_state.voice_recording:
            if st.button("Start", type="primary"):
                st.session_state.voice_recording = True
                st.session_state.voice_text = ""
                st.rerun()
        else:
            if st.button("Stop", type="secondary"):
                st.session_state.voice_recording = False
                st.rerun()

    # Handle voice recording
    if st.session_state.voice_recording:
        result_queue = queue.Queue()
        thread = Thread(target=listen_for_speech, args=(result_queue,))
        thread.start()
        
        with st.spinner("Listening..."):
            thread.join()
            try:
                result_type, result_value = result_queue.get_nowait()
                if result_type == "success":
                    st.session_state.voice_text = result_value
                    st.session_state.voice_recording = False
                    st.rerun()
                else:
                    st.error(result_value)
                    st.session_state.voice_recording = False
            except queue.Empty:
                st.error("No speech detected")
                st.session_state.voice_recording = False

def search_legal_query(query):
    """Function to handle the search operation"""
    with st.spinner('Searching...'):
        # Simulate search delay
        time.sleep(2)
        # Add your actual search logic here
        return f"Search results for: {query}"

# Custom CSS with theme support
def load_css():
    return """
    <style>
    /* Dark mode styles */
    [data-theme="dark"] {
        --bg-color: #1E1E1E;
        --text-color: #FFFFFF;
        --card-bg: #2D2D2D;
        --hover-color: #3D3D3D;
    }
    
    /* Light mode styles */
    [data-theme="light"] {
        --bg-color: #FFFFFF;
        --text-color: #1E1E1E;
        --card-bg: #F0F2F6;
        --hover-color: #E6E6E6;
    }
    
    /* Common styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .search-container {
        position: relative;
        margin: 20px auto;
        max-width: 600px;
    }
    
    .search-input {
        width: 100%;
        padding: 12px 45px 12px 15px;
        border: 2px solid var(--card-bg);
        border-radius: 10px;
        font-size: 16px;
        transition: all 0.3s ease;
        background: var(--bg-color);
        color: var(--text-color);
    }
    
    .search-input:focus {
        border-color: #0f5132;
        box-shadow: 0 0 0 3px rgba(15, 81, 50, 0.2);
    }
    
    .voice-button {
        position: absolute;
        right: 10px;
        top: 50%;
        transform: translateY(-50%);
        background: none;
        border: none;
        cursor: pointer;
        font-size: 20px;
        color: var(--text-color);
    }
    
    .search-button {
        display: block;
        margin: 15px auto;
        padding: 12px 30px;
        background-color: #0f5132;
        color: white;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .search-button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(15, 81, 50, 0.2);
    }
    
    .result-card {
        background: var(--card-bg);
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        transition: all 0.3s ease;
    }
    
    .result-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Loading animation */
    .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(15, 81, 50, 0.3);
        border-radius: 50%;
        border-top-color: #0f5132;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Feedback buttons */
    .feedback-buttons {
        display: flex;
        gap: 10px;
        justify-content: flex-end;
        margin-top: 10px;
    }
    
    .feedback-button {
        padding: 5px 10px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .feedback-button:hover {
        transform: scale(1.1);
    }
    </style>
    """

def initialize_autocomplete():
    """Initialize autocomplete suggestions"""
    return [
        "Indian Constitution Article",
        "Supreme Court judgments",
        "Legal rights in India",
        "Criminal procedure code",
        "Civil procedure code",
        "Legal documentation",
        # Add more suggestions
    ]

def show_search_interface():
    """Main search interface with autocomplete"""
    st.markdown(load_css(), unsafe_allow_html=True)
    
    
    # Theme toggle
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.toggle("🌗 Dark Mode", value=st.session_state.dark_mode):
            st.session_state.dark_mode = True
        else:
            st.session_state.dark_mode = False
    
    # Search container
    search_container = st.container()
    with search_container:
        # Autocomplete search
        query = st.text_input(
            "",
            placeholder="Enter your legal query here...",
            key="search_input"
        )
        
        # Show autocomplete suggestions
        if query:
            suggestions = [s for s in initialize_autocomplete() if query.lower() in s.lower()]
            if suggestions:
                selected_suggestion = st.selectbox("Suggestions:", suggestions)
                if selected_suggestion != query:
                    st.session_state.search_input = selected_suggestion
                    st.rerun()
        
        # Search button with animation
        if st.button("🔍 Search", key="search_button"):
            with st.spinner("Fetching results..."):
                time.sleep(1)  # Simulate search delay
                show_search_results(query)

def show_search_results(query):
    """Display search results in tabs"""
    # Add to search history
    if query:
        st.session_state.search_history.append({
            "query": query,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    # Create tabs for different result categories
    tab1, tab2, tab3 = st.tabs(["Case Laws", "Acts", "Amendments"])
    
    with tab1:
        show_result_card(
            "Case Law Result",
            "Sample case law content...",
            "case_law_1"
        )
    
    with tab2:
        show_result_card(
            "Act Result",
            "Sample act content...",
            "act_1"
        )
    
    with tab3:
        show_result_card(
            "Amendment Result",
            "Sample amendment content...",
            "amendment_1"
        )

def show_result_card(title, content, result_id):
    """Display a single result card with feedback buttons"""
    with st.container():
        st.markdown(f"""
            <div class="result-card">
                <h3>{title}</h3>
                <p>{content}</p>
                <div class="feedback-buttons">
                    <button class="feedback-button" onclick="feedback('{result_id}', 'up')">👍</button>
                    <button class="feedback-button" onclick="feedback('{result_id}', 'down')">👎</button>
                </div>
            </div>
        """, unsafe_allow_html=True)

def show_bookmarks():
    """Display bookmarked searches"""
    st.subheader("📌 Bookmarks")
    for bookmark in st.session_state.bookmarks:
        with st.expander(bookmark["query"]):
            st.write(f"Saved on: {bookmark['timestamp']}")
            if st.button("Remove", key=f"remove_{bookmark['timestamp']}"):
                st.session_state.bookmarks.remove(bookmark)
                st.rerun()

def show_history():
    """Display search history"""
    st.subheader("📜 Search History")
    for item in reversed(st.session_state.search_history[-10:]):
        with st.expander(item["query"]):
            st.write(f"Searched on: {item['timestamp']}")
            if st.button("Bookmark", key=f"bookmark_{item['timestamp']}"):
                st.session_state.bookmarks.append(item)
                st.rerun()

# ... (keep all imports and initial session state setup)

def main():
    # Initialize all session states in one place
    if 'show_main_content' not in st.session_state:
        st.session_state.show_main_content = True
    if 'show_voice_modal' not in st.session_state:
        st.session_state.show_voice_modal = False
    if 'show_profile' not in st.session_state:
        st.session_state.show_profile = False
    if 'voice_text' not in st.session_state:
        st.session_state.voice_text = ""
    if 'temp_search_text' not in st.session_state:
        st.session_state.temp_search_text = ""
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "home"

    # Apply CSS only once
    st.markdown(load_css(), unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.title("Legal Resources")
        st.markdown("---")
        
        if st.button("Indian Constitution", use_container_width=True):
            st.session_state.current_page = "constitution"
            
        if st.button("Today's Supreme Court Hearings", use_container_width=True):
            st.session_state.current_page = "sc_hearings"
            
        if st.button("Amendments", use_container_width=True):
            st.session_state.current_page = "amendments"
            
        if st.button("History", use_container_width=True):
            st.session_state.current_page = "history"

    # Profile button
    col1, col2 = st.columns([6,1])
    with col2:
        if st.button("👤 Profile"):
            st.session_state.show_profile = True
            st.session_state.show_main_content = False
            st.rerun()

    # Show either profile modal or main content
    if st.session_state.show_profile:
        show_profile_modal()
        if st.button("Close Profile"):
            st.session_state.show_profile = False
            st.session_state.show_main_content = True
            st.rerun()
    
    elif st.session_state.show_main_content:
        # Logo and title
        st.markdown("""
            <div style="text-align: center;">
                <h1>⚖️</h1>
                <h1>Nyyai Astra</h1>
                <h3>An AI-powered assistant for Indian legal queries.</h3>
            </div>
        """, unsafe_allow_html=True)

        # Search container with voice button inside
        with st.container():
            col1, col2 = st.columns([6,1])
            with col1:
                user_input = st.text_input(
                    "",
                    placeholder="Enter your legal query here...",
                    value=st.session_state.get('temp_search_text', ''),
                    key="search_input",
                    label_visibility="collapsed"
                )
                
                # Clear temp search text after using it
                if st.session_state.get('temp_search_text'):
                    st.session_state.temp_search_text = ""
            
            with col2:
                if st.button("🎤"):
                    st.session_state.show_voice_modal = True
                    st.rerun()

        # Search button centered below
        if st.button("🔍 Search", use_container_width=True):
            if user_input:
                show_search_results(user_input)

        # Voice search modal
        if st.session_state.show_voice_modal:
            show_voice_search_modal()
            if st.button("Close Voice Search"):
                st.session_state.show_voice_modal = False
                st.session_state.voice_recording = False
                st.rerun()

if __name__ == "__main__":
    main()