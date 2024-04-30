# libraries to import
import os
import PyPDF2
from openai import AzureOpenAI
from dotenv import load_dotenv
import os
import streamlit as st
from pathlib import Path

# load environment vars
load_dotenv()

# create a openai client
client = AzureOpenAI (
    api_key=os.getenv("OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    api_version=os.getenv("API_VERSION") # Ensure you use the correct API version
)


def analyze_cv (cv_text):
    try:
        # Make an API call to the ChatCompletion model
        prompt = "You are an expert recruiter and you must analyze the following resume and create a table with the technologies that the candidate has used, and the years of experience they have in each technology. The table must have the following structure [name, technology, years of experience] '{cv_text}'"
        response = client.chat.completions.create(
            model="gpt-35-turbo-0613", # Ensure the engine name is correct for your setup 
            messages=[{"role": "system", "content": prompt}]
        )    
        # Extract the message content from the response
        answer = response.choices[0].message.content
        return answer
    except Exception as e:
        return str(e) # Return the exception as a string for debugging 


def load_profiles():
    path = os.getenv("PROFILES_PATH")

    # loop over directory files
    for file in os.listdir(path):
        if file.endswith(".pdf"):  # check if the file has pdf extension
            path_file = os.path.join(path, file)
            with open(path_file, "rb") as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                cv_mess_text = ""
                # loop over PDF pages
                for page_number in range(len(pdf_reader.pages)):
                    cv_mess_text += pdf_reader.pages[page_number].extract_text()
                response = analyze_cv(cv_mess_text)
                st.chat_message("system").write(response)
                #texto_pdfs.append(texto)
    #return texto_pdfs        

def menu():
    st.title("💬 Chat Assistant")

    st.sidebar.subheader("About")
    st.sidebar.markdown("This is a chat interviewing application.")

    st.sidebar.subheader("Instructions")
    st.sidebar.markdown("Answer the questions asked by the interviewer using the chat interface.")

    st.sidebar.subheader("About Me")
    st.sidebar.markdown("I am an AI-powered interviewer, ready to ask you questions!")



if __name__ == "__main__":

    menu()
    load_profiles()


   