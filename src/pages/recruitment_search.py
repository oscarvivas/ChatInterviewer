# libraries to import
import os
from openai import AzureOpenAI
from dotenv import load_dotenv
import os
import streamlit as st
import menu_info
import chromadb
from chromadb.config import Settings
import re

# load environment vars
load_dotenv()

#Config Page
st.set_page_config(
    page_title="Seacrh Profile",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# create a openai client
client = AzureOpenAI (
    api_key=os.getenv("OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    api_version=os.getenv("API_VERSION") # Ensure you use the correct API version
)

# connect database
def connect_database():
    client_database = chromadb.PersistentClient(path="./database/", settings=Settings(allow_reset=True))
    return client_database


def extract_name(document):
    name = ""
    clean_text = document.replace("\n", "") 
    if re.search('Name:(.*)Core Skill', clean_text):
       name = re.search('Name:(.*)Core Skill', clean_text).group(1).strip()
    return name


def simple_request (messages_list):
    try:
        response = client.chat.completions.create(
            model="gpt-35-turbo-0613", # Ensure the engine name is correct for your setup 
            messages=messages_list
        )    
        # Extract the message content from the response
        answer = response.choices[0].message.content
        # print(answer)
        return answer
    except Exception as e:
        return str(e) # Return the exception as a string for debugging 


def analyze_resume (resume, position_description):
    try:
        # Make an API call to the ChatCompletion model
        prompt = f"""You are an expert recruiter,
You must analyze a resume and rate with a numerical value between 1 to 10 if the candidate meet with next job description '{position_description}', 
You should analyze the next resume '{resume}'
You should provide a rating between 1 to 10 if the candidate meet with job description
"""
        response = client.chat.completions.create(
            model="gpt-35-turbo-0613", # Ensure the engine name is correct for your setup 
            messages=[{"role": "assistant", "content": prompt}]
        )    
        # Extract the message content from the response
        answer = response.choices[0].message.content
        return answer
    except Exception as e:
        return str(e) # Return the exception as a string for debugging 



def initialize_chat():
    try:
        # Make an API call to the ChatCompletion model
        prompt = f"""You are a recruitment assistant, your job is to ask a series of questions to the user to identify the position you want to hire.
Chain of thought:
1. introduce yourself as a recruiting assistant willing to help search for a candidate
2. identify the [position] you want to hire
3. identify the [skills] that the candidate must have
4. identify whether which of the following values the candidate should have [Smart, Thoughtful, Open, Adaptable, Trusted]
5. generate a summary of position description and finalize the chat with the word searching"""
        response = client.chat.completions.create(
            model="gpt-35-turbo-0613", # Ensure the engine name is correct for your setup 
            messages=[{"role": "assistant", "content": prompt}]
        )    
        # Extract the message content from the response
        answer = response.choices[0].message.content
        return answer
    except Exception as e:
        return str(e) # Return the exception as a string for debugging 

def evaluate_profiles(position_description):
    client_database = connect_database()
    collection = client_database.get_collection(name="embedding_profiles")

    for document in [collection.get()["documents"][1]]:
        print(document)
        name = extract_name(document)
        result = analyze_resume (document, position_description)
        st.chat_message("assistant").write(name)
        st.chat_message("assistant").write(result)


def clean_chat():
    response = initialize_chat()
    st.session_state["messages"] = [{"role": "assistant", "content": response}]


if __name__ == "__main__":

    menu_info.menu_messages()

    #initilize position info
    position_description = ""

    if st.button('Clean Chat'):
        clean_chat()

    if "messages" not in st.session_state:
        response = initialize_chat()
        st.session_state["messages"] = [{"role": "assistant", "content": response}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])


    if (prompt := st.chat_input()) and (position_description == ""):

        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        response = simple_request (st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)

        if ('searching' in response) or ('search' in prompt):
            position_description = response
            print('Success!\n' + position_description)
            evaluate_profiles(position_description)
   