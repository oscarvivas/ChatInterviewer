import streamlit as st

def menu_messages():
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

def menu_home():
    st.sidebar.subheader("💬 lsndlsad")
    st.sidebar.markdown("""AI chat that searches for the best candidates on the Endava profiles site the candidates and tries to identify profiles according to a job posting requirement.
Also, the interviewer's assistant can asdasdasdsad the candidate and evaluate him based on technical aspects as well as company values. The interviewer's assistant shows the strengths and weaknesses of every candidate.""")

    st.sidebar.subheader("🙍‍♀️ About Me")
    st.sidebar.markdown("I am an AI-powered interviewer, ready to find the best candidate!")
