# libraries to import
from dotenv import load_dotenv
import streamlit as st

st.set_page_config(
    page_title="HADA - Hiring Assistant for enDAva",
    page_icon="🧚‍♀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# load environment vars
load_dotenv()

def body():
    st.title("🧚‍♀️ HADA - Hiring Assistant for enDAva")
    st.text("some text")
    st.code("no te olvides de poner el where en el delete from")


def menu():
    st.sidebar.subheader("💬 About")
    st.sidebar.markdown("""AI chat that searches for the best candidates on the Endava profiles site the candidates and tries to identify profiles according to a job posting requirement.
Also, the interviewer's assistant can interview the candidate and evaluate him based on technical aspects as well as company values. 
At the end of the interview, the interviewer's assistant shows the strengths and weaknesses of every candidate. Also, the chat includes options for transforming results from text to speech.
At the end, you can see a dashboard with insights from every candidate.""")

    st.sidebar.subheader("👉 Instructions")
    st.sidebar.markdown("""1. Load the Endava profiles into the database.
                           2. Request a best profilefor specific position
                           3. See the candidates into the candidate dashboard
                           4. I interview the candidate
                           5. See the results in the final dashboard""")

    st.sidebar.subheader("🙍‍♀️ About Me")
    st.sidebar.markdown("I am an AI-powered interviewer, ready to find the best candidate!")


if __name__ == "__main__":
    body()
    menu()



   