import streamlit as st
import speech_recognition as sr
import time
import random

def set_theme():
    if "theme" not in st.session_state:
        st.session_state.theme = "light"
    theme_css = """
    <style>
    body {font-family: 'Inter', sans-serif;}
    .dark-theme {background-color: #1e1e1e; color: white;}
    .light-theme {background-color: white; color: black;}
    .search-button:hover {animation: pulse 1s infinite;}
    @keyframes pulse {
      0% {box-shadow: 0 0 5px rgba(0,0,0,0.2);}
      50% {box-shadow: 0 0 15px rgba(0,0,0,0.4);}
      100% {box-shadow: 0 0 5px rgba(0,0,0,0.2);}
    }
    </style>
    """
    st.markdown(theme_css, unsafe_allow_html=True)
    theme_class = "dark-theme" if st.session_state.theme == "dark" else "light-theme"
    return theme_class

def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Could not understand the audio."
        except sr.RequestError:
            return "Could not request results."

def fetch_results(query):
    time.sleep(2)  # Simulating a search delay
    return {"Case Laws": f"Results for {query} in Case Laws", "Acts": f"Results for {query} in Acts"}

st.set_page_config(page_title="Nyyai Astra", layout="wide")
theme_class = set_theme()

st.sidebar.button("Toggle Dark/Light Mode", on_click=toggle_theme)

st.title("⚖️ Nyyai Astra - AI Legal Assistant")
query = st.text_input("Enter your legal query", placeholder="Search legal cases, acts...")
voice_search = st.button("🎙️ Voice Search")

if voice_search:
    query = recognize_speech()
    st.text_input("Recognized Text", value=query)

if st.button("🔍 Search", key="search_button", help="Search Legal Database"):
    with st.spinner("Fetching results..."):
        results = fetch_results(query)
    tabs = st.tabs(["Case Laws", "Acts"])
    for i, (key, value) in enumerate(results.items()):
        with tabs[i]:
            st.write(value)
            st.button("👍", key=f"up_{key}")
            st.button("👎", key=f"down_{key}")

st.subheader("📌 Bookmarks & History")
st.write("Feature Coming Soon!")

st.subheader("📄 PDF Upload & Analysis")
file = st.file_uploader("Upload Legal Document")
if file:
    st.write("Processing file...")
    time.sleep(2)
    st.success("Key Legal Terms Highlighted!")

st.subheader("🤖 Chatbot Mode")
chat_input = st.chat_input("Ask Nyyai Astra...")
if chat_input:
    st.write(f"You: {chat_input}")
    st.write("Bot: Feature in development!")
