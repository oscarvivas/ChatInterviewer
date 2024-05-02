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


def analyze_resume (resume, skills, values):
    try:
        # Make an API call to the ChatCompletion model
        prompt = f"""You are an expert recruiter,
You must analyze a resume and rate with a numerical value between 1 to 10 if the candidate have the next skills '{skills}', 
Also, you should rate with a numerical value between 1 to 10 if the candidate meet the next company values '{values}', 
You should analyze the next resume '{resume}'
You should use the next example to format the results
name: pedro perez
skills: 8.5
values: 7.3
"""
        response = client.chat.completions.create(
            model="gpt-35-turbo-0613", # Ensure the engine name is correct for your setup 
            messages=[{"role": "system", "content": prompt}]
        )    
        # Extract the message content from the response
        answer = response.choices[0].message.content
        return answer
    except Exception as e:
        return str(e) # Return the exception as a string for debugging 


def step1_introduce_assitent():
    try:
        # Make an API call to the ChatCompletion model
        prompt = "You are an assistant for recruitment, your job is help to the recruiter, introduce yourself as a recruiting assistant willing to help search for a candidate and ask what position the recruiter wants to hire"
        response = client.chat.completions.create(
            model="gpt-35-turbo-0613", # Ensure the engine name is correct for your setup 
            messages=[{"role": "system", "content": prompt}]
        )    
        # Extract the message content from the response
        answer = response.choices[0].message.content
        return answer
    except Exception as e:
        return str(e) # Return the exception as a string for debugging 

def step2_identify_position(description):
    try:
        # Make an API call to the ChatCompletion model
        prompt = f"You are an expert in recruitment, your job is help to the recruiter identify the position that the recruiter wants to hire using the next description '{description}'"
        response = client.chat.completions.create(
            model="gpt-35-turbo-0613", # Ensure the engine name is correct for your setup 
            messages=[{"role": "system", "content": prompt}]
        )    
        # Extract the message content from the response
        answer = response.choices[0].message.content
        return answer
    except Exception as e:
        return str(e) # Return the exception as a string for debugging 


def step3_identify_skills(position, description):
    try:
        # Make an API call to the ChatCompletion model
        prompt = f"You are an expert in recruitment, your job is help to the recruiter identify the skills that the candidate should have for the position {position} using the next description {description}"
        response = client.chat.completions.create(
            model="gpt-35-turbo-0613", # Ensure the engine name is correct for your setup 
            messages=[{"role": "system", "content": prompt}]
        )    
        # Extract the message content from the response
        answer = response.choices[0].message.content
        return answer
    except Exception as e:
        return str(e) # Return the exception as a string for debugging 


def step3_identify_values(position, description):
    try:
        # Make an API call to the ChatCompletion model
        prompt = f"You are an expert in recruitment, your job is help to the recruiter identify the next company values the candidate should meet [Smart, Thoughtful, Open, Adaptable, Trusted] for the position {position} using the next description {description}"
        response = client.chat.completions.create(
            model="gpt-35-turbo-0613", # Ensure the engine name is correct for your setup 
            messages=[{"role": "system", "content": prompt}]
        )    
        # Extract the message content from the response
        answer = response.choices[0].message.content
        return answer
    except Exception as e:
        return str(e) # Return the exception as a string for debugging 
    

def step4_evaluate_profiles():
    client_database = connect_database()
    collection = client_database.get_collection(name="embedding_profiles")

    for document in collection.get()["documents"][1]:
        name = extract_name(document)
        result = analyze_resume (document, skills, values)
        st.chat_message("assistant").write(name)
        st.chat_message("assistant").write(result)



def request_position_data():

    #introduce the assistent
    response = step1_introduce_assitent()
    st.chat_message("assistant").write(response)

    #identify position
    if user_input := st.chat_input():
        position = step2_identify_position(user_input)
        print(position)
        st.chat_message("user").write(user_input)

        #identify skills
        st.chat_message("assistant").write("What technical skills are essential for this position?")

    if user_input := st.chat_input():
        skills = step3_identify_skills(position, user_input)
        print(skills)
        st.chat_message("user").write(user_input)

        #identify values
        st.chat_message("assistant").write("Which of the following values are important for the candidate to possess: Smart, Thoughtful, Open, Adaptable, Trusted?")

    if user_input := st.chat_input():
        values = step3_identify_values(position, user_input)
        print(values)
        st.chat_message("user").write(user_input)

        # search candidate
        st.chat_message("assistant").write("Great! With that information, I'll begin the search for suitable candidates.")
        st.chat_message("assistant").write("Searching ...")
    
        step4_evaluate_profiles()



if __name__ == "__main__":

    menu_info.menu_messages()

    #initilize position info
    position = ""
    skills = []
    values = []

    if st.button('Start candidate search'):
        request_position_data()

   