import streamlit as st
from streamlit_app import summerise
from streamlit_extras.add_vertical_space import add_vertical_space
from data import get_collection, insert_data, get_data
import re

st.set_page_config(page_title="PDF Summarizer & Q&A", layout="wide")

# Function to add local background image
def add_bg_from_local(image_path):
    css = f"""
    <style>
    body {{
        background-image: url("{image_path}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Add background image from local file
# add_bg_from_local("D:/Project/PdfSummeriser_Q-A_langchain/website.jpg")

# Top Navigation Menu
st.markdown("<h1 style='text-align: center;'>Docsift Intelligent App</h1>", unsafe_allow_html=True)
menu = ["Create Account", "Login/Signup", "Home", "Contact"]
choice = st.radio("Navigation", menu, horizontal=True)

st.markdown("---")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Handle page navigation
if choice == "Create Account":
    st.markdown("#### Create Account #################################")
    st.markdown("This section will allow users to create a new account.")

    collection = get_collection()
    if collection is not None:
        # Placeholder for Create Account form
        with st.form(key='create_account_form'):
            new_username = st.text_input('New Username')
            new_password = st.text_input('New Password', type='password')
            create_account_button = st.form_submit_button(label='Create Account')
            if create_account_button:
                existing_user = collection.find_one({"username": new_username})
                if existing_user:
                    st.warning("Username already exists. Please log in instead.")
                else:
                    new_user_data = {"username": new_username, "password": new_password}
                    insert_data(collection, new_user_data)
                    st.success(f"Account created for {new_username}. Please log in.")

elif choice == "Login/Signup":
    st.markdown("#### Login/Signup #################################")
    st.markdown("This section will contain login/signup functionalities.")

    collection = get_collection()
    if collection is not None:
        # Placeholder for Login form
        with st.form(key='login_form'):
            username = st.text_input('Username')
            password = st.text_input('Password', type='password')
            submit_button = st.form_submit_button(label='Login')
            if submit_button:
                user_data = collection.find_one({"username": username, "password": password})
                if user_data:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success(f"Logged in as {username}")
                else:
                    st.error("Invalid username or password")

elif choice == "Home":
    if st.session_state.logged_in:
        st.markdown("#### Summarizer & Q&A #################################")
        st.markdown("""
            This is a summarizer and Q&A tool for PDF and DOCX files. Upload your document and get a summary along with the ability to ask questions about the content.
        """)
        summerise()
    else:
        st.warning("You need to log in to access this page.")
        st.session_state["choice"] = "Login/Signup"

elif choice == "Contact":
    st.markdown("#### Contact #################################")
    st.markdown("This section will contain contact information and a form to get in touch.")

    collection = get_collection()
    if collection is not None:
        # Placeholder for Contact form
        with st.form(key='contact_form'):
            name = st.text_input('Name')
            email = st.text_input('Email')
            message = st.text_area('Message')
            submit_button = st.form_submit_button(label='Send')
            if submit_button:
                # Email validation
                email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
                if re.match(email_pattern, email):
                    contact_data = {"name": name, "email": email, "message": message}
                    insert_data(collection, contact_data)
                    st.success("Your message has been sent successfully!")
                else:
                    st.error("Invalid email address. Please enter a valid email.")

# Add Logout button
if st.session_state.logged_in:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.success("Logged out successfully")

# Footer
add_vertical_space(5)
st.write('© Tech_Titans')
