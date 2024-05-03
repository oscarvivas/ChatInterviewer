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
import pandas as pd

# load environment vars
load_dotenv()

#Config Page
st.set_page_config(
    page_title="Search Profile",
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
            model=os.getenv("OPENAI_MODEL"), # Ensure the engine name is correct for your setup 
            messages=messages_list
        )    
        # Extract the message content from the response
        answer = response.choices[0].message.content
        # print(answer)
        return answer
    except Exception as e:
        return str(e) # Return the exception as a string for debugging 


def extract_percentage(response):
    last_line = response.splitlines()[-1]
    print(last_line)
    percentage = re.findall('[0-9]+%', last_line)[0]
    print(percentage)
    return percentage


def analyze_resume (resume, position_description):
    try:
        # Make an API call to the ChatCompletion model
        prompt = f"""You are an expert recruiter,
        You should use the next resume '{resume}'
        And identify if the candidate meets with next job description '{position_description}', 

        Chain of thought:
        1. You should count the skills that the job description has
        2. You should count what job description's skills are contained  in the resume 
        3. You should divide the number in the previous step by the number in the first step and show the result in a bullet.
"""
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL"), # Ensure the engine name is correct for your setup 
            messages=[{"role": "assistant", "content": prompt}]
        )    
        # Extract the message content from the response
        # print(response)
        if len(response.choices) > 0:
            answer = response.choices[0].message.content
            answer = extract_percentage(answer)
        else:
            answer = "0%"
        return answer
    except Exception as e:
        print(str(e)) # Return the exception as a string for debugging 
        return "0%" 


def delete_collection(collection_name):
    client_database = connect_database()

    # delete if exits
    if collection_name in [c.name for c in client_database.list_collections()]:
        client_database.delete_collection(name=collection_name)



def store_rating_candidates (ids, metadatas, documents):
    try:
        client_database = connect_database()

        collection_name = "candidate_rating"
        # delete if exits
        if collection_name in [c.name for c in client_database.list_collections()]:
            client_database.delete_collection(name=collection_name)

        collection = client_database.get_or_create_collection(name=collection_name)
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        return collection

    except Exception as e:
        print(str(e))
        return str(e) # Return the exception as a string for debugging 


def initialize_chat():
    try:
        # Make an API call to the ChatCompletion model
        prompt = f"""You are a recruitment assistant, your job is to ask the recruiter who needs your help, a series of questions to identify the position that the recruiter wants to hire.
        Chain of thought:
        1. introduce yourself as a recruiting assistant to the recruiter, telling that you are willing to help searching for a candidate
        2. identify the [position] that the recruiter needs to hire
        3. identify the [skills] that the potential candidate must have
        4. identify from the following company values [Smart, Thoughtful, Open, Adaptable, Trusted] which ones the potential candidates have
        5. then finally, generate a summary of position description and finalize the chat with the word "Searching"
        This  is your only role, you have to follow the chain of thought mentioned before and you can not do anything else."""
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL"), # Ensure the engine name is correct for your setup 
            messages=[{"role": "assistant", "content": prompt}],
            temperature=0
        )    
        # Extract the message content from the response
        answer = response.choices[0].message.content
        return answer
    except Exception as e:
        return str(e) # Return the exception as a string for debugging 

def evaluate_profiles(position_description):
    
    id = 0
    ids = []
    documents = []
    metadatas = []

    client_database = connect_database()
    collection = client_database.get_collection(name="embedding_profiles")

    for document in collection.get()["documents"]:
        name = extract_name(document)
        result = analyze_resume (document, position_description)

        if result != "0%":

            result = result.replace("%", "")

            id += 1
            ids.append("id"+ str(id))

            document = f"name: {name} rating: {result}"
            documents.append(document)

            source = {}
            source["source"] = name
            metadatas.append(source)        

            #st.chat_message("assistant").write(name)
            st.chat_message("assistant").write(document)


    collection = store_rating_candidates(ids, metadatas, documents)
    st.chat_message("assistant").write(f"{id} Profiles were analized, please check the candidate dashboard!!")

    data = get_candidate_data(collection)
    show_data(data)


def get_candidate_data(collection):
    data = {"name":[], "Rate":[]}
    for document in collection.get()["documents"]:
        try:
            name = ""
            rating = 0

            if re.search('name:(.*)rating:', document):
                name = re.search('name:(.*)rating:', document).group(1).strip()

            if re.search('rating:(.*)', document):
                rating = re.search('rating:(.*)', document).group(1).strip()

            data["name"].append(name)
            data["Rate"].append(rating)
        except Exception as e:
            print("Error " + str(e) + " no actions")
    return data

    
def show_data(data):
    dataframe = pd.DataFrame(data)
    dataframe = dataframe.set_index("name")
    st.bar_chart(dataframe)
    

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
   