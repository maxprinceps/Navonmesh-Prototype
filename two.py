import streamlit as st
import streamlit.components.v1 as components

# Step 1: Initialize session state for profile modal
if "show_profile" not in st.session_state:
    st.session_state.show_profile = False  # Initially hidden

# Step 2: Define a function to toggle profile modal
def toggle_profile():
    st.session_state.show_profile = not st.session_state.show_profile

# Step 3: Use Markdown to position the Profile button in the top-right corner
st.markdown(
    """
    <style>
        .profile-button {
            position: absolute;
            top: 10px;
            right: 20px;
            background-color: #007BFF;
            color: white;
            padding: 8px 15px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            z-index: 999;
        }
        .profile-button:hover {
            background-color: #0056b3;
        }
    </style>
    <button class="profile-button" onclick="toggleProfile()">Profile</button>
    <script>
        function toggleProfile() {
            var element = window.parent.document.getElementById('profile-content');
            if (element.style.display === "none") {
                element.style.display = "block";
            } else {
                element.style.display = "none";
            }
        }
    </script>
    """,
    unsafe_allow_html=True
)

# Step 4: Load the login form in a responsive popup/modal
if st.session_state.show_profile:
    try:
        # Read the HTML file
        with open("login.html", "r", encoding="utf-8") as f:
            login_html = f.read()

        # Apply CSS styles in Streamlit for responsiveness
        modal_style = """
            <style>
                #profile-content {
                    position: fixed;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    width: 90%;
                    max-width: 400px;
                    height: auto;
                    background-color: white;
                    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
                    padding: 20px;
                    border-radius: 10px;
                    z-index: 1000;
                    display: block;
                }
                .overlay {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background-color: rgba(0, 0, 0, 0.5);
                    z-index: 999;
                }
            </style>
        """
        
        # Wrap the login form inside a modal
        modal_html = f"""
            {modal_style}
            <div class="overlay" onclick="toggleProfile()"></div>
            <div id="profile-content">
                {login_html}
            </div>
        """

        # Render the modal inside Streamlit
        components.html(modal_html, height=600, scrolling=False)

    except Exception as e:
        st.error(f"Error loading login form: {e}")
