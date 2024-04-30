# libraries to import
from dotenv import load_dotenv
import streamlit as st
from st_pages import Page, show_pages, add_page_title

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
        Page("src/pages/recruitment_app.py", "HADA Recruiter", "🧚"),
        Page("src/pages/load_profiles.py", "Profile Loader", ":book:"),
        Page("src/pages/recruitment_search.py", "Recruitment Search", "🔎"),
        Page("src/pages/dashboard.py", "Dashboard", "📊"),
    ]
)

# load environment vars
load_dotenv()

def body():
    st.image('images/endava_logo.jpg', caption='Technology is our how. And people are our why.')
    st.title("🧚‍♀️ HADA - Hiring Assistant for Endava")
    st.text("👉 Instructions")
    st.code("1. Load the Endava profiles into the database.")
    st.code("2. Request a best profilefor specific position.")
    st.code("3. See the candidates into the candidate dashboard.")
    st.code("4. I interview the candidate.")
    st.code("5. See the results in the final dashboard.")

def menu():
    st.sidebar.subheader("💬 About")
    st.sidebar.markdown("""AI chat that searches for the best candidates on the Endava profiles site the candidates and tries to identify profiles according to a job posting requirement.
Also, the interviewer's assistant can interview the candidate and evaluate him based on technical aspects as well as company values. 
At the end of the interview, the interviewer's assistant shows the strengths and weaknesses of every candidate.""")

    st.sidebar.subheader("🙍‍♀️ About Me")
    st.sidebar.markdown("I am an AI-powered interviewer, ready to find the best candidate!")


if __name__ == "__main__":
    body()
    menu()



   