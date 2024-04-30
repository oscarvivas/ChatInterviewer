# libraries to import
import os
import PyPDF2
from openai import AzureOpenAI
from dotenv import load_dotenv
import os
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="IA Recruitment Home",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# load environment vars
load_dotenv()

def body():
    st.title("💬 Chat Assistant")
    st.text("some text")
    st.code("no te olvides de poner el where en el delete from")

def menu():
    

    st.sidebar.subheader("About")
    st.sidebar.markdown("This is a chat interviewing application.")

    st.sidebar.subheader("Instructions")
    st.sidebar.markdown("Answer the questions asked by the interviewer using the chat interface.")

    st.sidebar.subheader("About Me")
    st.sidebar.markdown("I am an AI-powered interviewer, ready to ask you questions!")



if __name__ == "__main__":
    body()
    menu()



   