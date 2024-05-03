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
        Page("src/pages/recruitment_search.py", "HADA Candidate Finder", "🧚"),
        Page("src/pages/dashboard_candidates.py", "Candidates Dashboard", "📊"),
        Page("src/pages/recruitment_interview.py", "HADA Interview Analyzer", "🧚"),
        Page("src/pages/dashboard_interview.py", "Interview Dashboard", "📊"),
    ]
)

def menu_home():
    st.sidebar.subheader("💬 About")
    st.sidebar.markdown("""Hiring Assistant for Endava is an application designed to help in the process of recruiting new talents. 
                        HADA Candidate Finder will search and read the different profiles. Pinpointing the most suitable candidates based on the search requirements.
                        HADA Interview Analizer will perform an analysis of the interview by the recruiter and the candidates. Also, will provide a comprehensive assessment of each candidate's strengths and weaknesses.""")

    st.sidebar.subheader("🙍‍♀️ About Me")
    st.sidebar.markdown("I am an AI-powered interviewer, ready to find the best candidate!")

def menu_message():
    st.sidebar.subheader("📍 Instructions")
    st.sidebar.markdown(""" 
    1. Upload the profiles into the repository.
    2. In Profile Loader you check the profiles in the database.
    3. Chat with HADA Candidate Finder to refine your candidate search.
    4. With the Candidates Dashboard look up the chart with the candidates.
    5. HADA Interview Analyzer can deliver another insight from the interview to the candidates.
    6. In the Interview Dashboard check the chart for the interview results.""")

    st.sidebar.subheader("🙍‍♀️ About Me")
    st.sidebar.markdown("I am an AI-powered interviewer, ready to find the best candidate!")


def body():
    st.image('images/endava_logo.jpg', caption='Technology is our how. And people are our why.')
    st.title("🧚‍♀️ HADA - Hiring Assistant for Endava")
    st.text("👉 Instructions:")
    st.code("1. Upload the profiles into the repository.")
    st.code("2. In Profile Loader you check the profiles in the database.")
    st.code("3. Chat witg HADA Candidate Finder to refine your candidate search")
    st.code("4. With the Candidates Dashboard look up the chart with the candidates")
    st.code("5. HADA Interview Analyzer can deliver another insight from the interview to the candidates.")
    st.code("6. In the Interview Dashboard check the chart for the interview results.")
    st.code("Developed with ❤️ for Endava")

if __name__ == "__main__":
    menu_home()
    body()



   