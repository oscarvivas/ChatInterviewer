# libraries to import
from dotenv import load_dotenv
import streamlit as st
from st_pages import Page, show_pages, add_page_title

# load environment vars
load_dotenv()

#Config Page
st.set_page_config(
    page_title="HADA - Hiring Assistant for Endava",
    page_icon="🧚‍♀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Specify what pages should be shown in the sidebar, and what their titles and icons should be
show_pages(
    [
        Page("src/main.py", "Home", "🏠"),
        Page("src/pages/uploader_files.py", "File Uploader", "📂"),
        Page("src/pages/load_profiles.py", "Profile Loader", ":book:"),
        Page("src/pages/recruitment_search.py", "Search Candidates", "🔎"),
        Page("src/pages/dashboard_candidates.py", "Dashboard Candidates", "📊"),
        Page("src/pages/recruitment_interview.py", "HADA Recruiter Interview", "🧚"),
        Page("src/pages/dashboard_interview.py", "Dashboard Interview", "📊"),
    ]
)

def menu_messages():
    st.sidebar.subheader("💬 About")
    st.sidebar.markdown("""AI chat that searches for the best candidates on the Endava profiles site the candidates and tries to identify profiles according to a job posting requirement.
Also, the interviewer's assistant can interview the candidate and evaluate him based on technical aspects as well as company values. The interviewer's assistant shows the strengths and weaknesses of every candidate.""")

    st.sidebar.subheader("🙍‍♀️ About Me")
    st.sidebar.markdown("I am an AI-powered interviewer, ready to find the best candidate!")

def menu_home():
    st.sidebar.subheader("💬 lsndlsad")
    st.sidebar.markdown("""AI chat that searches for the best candidates on the Endava profiles site the candidates and tries to identify profiles according to a job posting requirement.
Also, the interviewer's assistant can asdasdasdsad the candidate and evaluate him based on technical aspects as well as company values. The interviewer's assistant shows the strengths and weaknesses of every candidate.""")

    st.sidebar.subheader("🙍‍♀️ About Me")
    st.sidebar.markdown("I am an AI-powered interviewer, ready to find the best candidate!")


def body():
    st.image('images/endava_logo.jpg', caption='Technology is our how. And people are our why.')
    st.title("🧚‍♀️ HADA - Hiring Assistant for Endava")
    st.text("👉 Instructions:")
    st.code("1. Load the Endava profiles into the database.")
    st.code("2. Request a best profile for specific position.")
    st.code("3. See the candidates into the candidate dashboard.")
    st.code("4. Make the interview for the candidate.")
    st.code("5. See the results on the final dashboard.")
    st.code("Developed with ❤️ for Endava")

if __name__ == "__main__":
    menu_home()
    body()



   