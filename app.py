import streamlit as st
import requests

def query_indian_kanoon(search_query):
    # Placeholder function for API integration (modify when you get API access)
    return f"Results for: {search_query}\n\n(Sample response from Indian Kanoon)"

def main():
    st.set_page_config(page_title="Nyyai Astra - Legal AI", layout="centered")
    
    # Centered Layout
    st.markdown("""
        <div style="text-align: center;">
            <h1>⚖️</h1>
            <h1>Nyyai Astra</h1>
            <h3>An AI-powered assistant for Indian legal queries.</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Centered Search Box and Button
    user_query = st.text_input("", placeholder="Ask your legal question...", key="query")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Search", key="search_button", help="Click to search", use_container_width=True):
            if user_query.strip():
                response = query_indian_kanoon(user_query)
                st.text_area("Response:", response, height=200)
            else:
                st.warning("Please enter a valid query.")

if __name__ == "__main__":
    main()
