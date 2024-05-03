# libraries to import
import os
import streamlit as st
from dotenv import load_dotenv
from openai import AzureOpenAI
import PyPDF2
import menu_info
import re
import chromadb
from chromadb.config import Settings

# connect database
def connect_database():
    client_database = chromadb.PersistentClient(path="./database/", settings=Settings(allow_reset=True))
    return client_database

#Config Page
st.set_page_config(
    page_title="Profile Loader",
    page_icon="book",
    layout="wide",
    initial_sidebar_state="expanded"
)

# load environment vars
load_dotenv()

# create a openai client
client = AzureOpenAI (
    api_key=os.getenv("OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    api_version=os.getenv("API_VERSION") # Ensure you use the correct API version
)

def extract_name(document):
    name = ""
    clean_text = document.replace("\n", "") 
    if re.search('Name:(.*)Core Skill', clean_text):
       name = re.search('Name:(.*)Core Skill', clean_text).group(1).strip()
    return name

def store_embedding (ids, metadatas, documents):
    try:
        client_database = connect_database()
        client_database.reset()
        collection = client_database.get_or_create_collection(name="embedding_profiles")
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        #print(collection.get()["documents"])

    except Exception as e:
        print(e)
        return str(e) # Return the exception as a string for debugging 


def extract_data_cv (cv_text):
    try:
        # Make an API call to the ChatCompletion model
        prompt = f"""You are an expert in recruitment, 

you should extract the name, core skill, English level, technologies, and soft skills from the resume

Also, you should seek the candidate's skills and match them with the company values: 
* Smart: We employ clever people who bring skills, experience, and talent to craft smart solutions for our customers. 
* Thoughtful: We care deeply about people, whether they are our employees, customers, or our broader communities.
* Open: We have confidence in our abilities, approach, and people, so we are open and transparent.
* Adaptable: We embrace change and remain flexible, allowing us to operate successfully in complex environments.
* Trusted: We build our relationships on trust and integrity. 
and rate every value with the next values: low, medium, or high

You should generate the result in text format 

You should use the next resume '{cv_text}'
"""
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL"), # Ensure the engine name is correct for your setup 
            messages=[{"role": "system", "content": prompt}]
        )    
        # Extract the message content from the response
        answer = response.choices[0].message.content
        return answer
    except Exception as e:
        print(e)
        return str(e) # Return the exception as a string for debugging 



def load_profiles():
    path = os.getenv("PROFILES_PATH")
    #profiles_list = [os.listdir(path)[0], os.listdir(path)[1]]
    profiles_list = os.listdir(path)
    id = 0

    ids = []
    documents = []
    metadatas = []

    st.chat_message("assistant").write(f"loading Profiles...")

    # loop over directory files
    for file in profiles_list:

        if file.endswith(".pdf"):  # check if the file has pdf extension
            path_file = os.path.join(path, file)

            print(path_file)

            with open(path_file, "rb") as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                cv_mess_text = ""

                # loop over PDF pages
                for page_number in range(len(pdf_reader.pages)):
                    cv_mess_text += pdf_reader.pages[page_number].extract_text()
                
                response = extract_data_cv(cv_mess_text)
                documents.append(response)
                name = extract_name(response)
                source = {}
                source["source"] = name
                metadatas.append(source)

                id += 1
                ids.append("id"+ str(id))

    store_embedding(ids, metadatas, documents)
    st.chat_message("assistant").write(f"{id} Profiles were loaded.")



def show_profiles():
    client_database = connect_database()
    collection = client_database.get_collection(name="embedding_profiles")

    for document in collection.get()["documents"]:
        name = extract_name(document)
        st.chat_message("assistant").write(name)
        st.chat_message("assistant").write(document)

    #for element in collection.get()["metadatas"]:
    #    st.chat_message("assistant").write(element)



if __name__ == "__main__":

    menu_info.menu_messages()
    
    if st.button('Load Profiles'):
        load_profiles()

    if st.button('Show Profiles'):
        show_profiles()

