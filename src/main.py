# libraries to import
from dotenv import load_dotenv
import streamlit as st

st.set_page_config(
    page_title="HADA - Hiring Assistant for Endava",
    page_icon="🧚‍♀️",
    layout="wide",
    initial_sidebar_state="expanded"
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



   