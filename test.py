import streamlit as st
import requests

st.set_page_config(page_title="Nyyai Astra - Legal AI", layout="centered")

def query_indian_kanoon(search_query):
    # Placeholder function for API integration (modify when you get API access)
    return f"Results for: {search_query}\n\n(Sample response from Indian Kanoon)"

def main():
    # Add custom CSS for button hover color
    st.markdown("""
        <style>
        .stButton button:hover {
            background-color: #0000
            !important;
            border-color: #4ca1af !important;
            color: white !important;
            border-width: 2px
        }
        </style>
    """, unsafe_allow_html=True)
    
    
    
    # Add sidebar
    with st.sidebar:
        st.title("Legal Resources")
        st.markdown("---")
        
        if st.button("The Constitution of India", use_container_width=True):
            st.session_state.current_page = "constitution"
            
        if st.button("Today's Supreme Court Hearings", use_container_width=True):
            st.session_state.current_page = "sc_hearings"
            
        if st.button("Amendments", use_container_width=True):
            st.session_state.current_page = "amendments"
            
        if st.button("History", use_container_width=True):
            st.session_state.current_page = "history"
    
    # Add profile button in top right
    col_space, col_profile = st.columns([4, 1])
    with col_profile:
        if st.button("👤 Profile"):
            st.session_state.show_profile = True
    
    # Main content
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
