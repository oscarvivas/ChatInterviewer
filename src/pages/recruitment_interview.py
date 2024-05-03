# libraries to import
from openai import AzureOpenAI
from dotenv import load_dotenv
import os
import streamlit as st
import menu_info
import chromadb
import re
import pandas as pd
import matplotlib.pyplot as plt

#Config Page
st.set_page_config(
    page_title="HADA Interview Analyzer",
    page_icon="🧚‍♀️",
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

# connect database
def connect_database():
    client_database = chromadb.PersistentClient(path="./database/", settings=Settings(allow_reset=True))
    return client_database


position = ".Net developer"

prompt = f"""Generate an interview between a Human Resources (HR) recruiter and a candidate for the {position} position. The interview should address both technical and soft skills and contain a maximum of 10 questions and answers."""
prompt_analize = f"""You are an expert in recruitment, 
You should analize a job interview conducted to a {position} and
you should analize the skills and match them with the company values: 
* Smart: We employ clever people who bring skills, experience, and talent to craft smart solutions for our customers. 
* Thoughtful: We care deeply about people, whether they are our employees, customers, or our broader communities.
* Open: We have confidence in our abilities, approach, and people, so we are open and transparent.
* Adaptable: We embrace change and remain flexible, allowing us to operate successfully in complex environments.
* Trusted: We build our relationships on trust and integrity. 
and rate every value with the next values: low, medium, or high
You should generate the result in text format 
You should generate a list of bullets with value and rating take into account the next exmaple
* Smart: low
* Thoughtful: low
* Open: low
* Adaptable: low
* Trusted: low """

final_values = []
final_qualifications = []

def interview():

    if "messages2" not in st.session_state:
        initalize_chat()

    user_input = st.chat_input()
    if user_input: 
        st.session_state["messages2"].append({"role": "user", "content": user_input }) 

       
    for msg in st.session_state["messages2"]:
        st.chat_message(msg["role"]).write(msg["content"])



def generate_interview (chatMessages):
    try:
        # Make an API call to the ChatCompletion model
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL"), # Ensure the engine name is correct for your setup 
            messages=chatMessages
        )    
        # Extract the message content from the response
        answer = response.choices[0].message.content
        return answer
    except Exception as e:
        return str(e) # Return the exception as a string for debugging 
    

def analize_interview (interview):
    try:
        # Make an API call to the ChatCompletion model
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL"), # Ensure the engine name is correct for your setup 
            messages=[{"role": "assistant", "content": f"{prompt_analize} '{interview}'"}]
        )    
        # Extract the message content from the response
        answer = response.choices[0].message.content
        return answer
    except Exception as e:
        return str(e) # Return the exception as a string for debugging 


def initalize_chat():

    st.chat_message("assistant").write(f"Generating Interview ....")

    responseMessage = generate_interview([{"role": "assistant", "content": prompt}])
    st.session_state["messages2"] = [{"role": "assistant", "content": responseMessage}]

    st.chat_message("assistant").write(f"Analizing Interview ....")

    responseMessage = analize_interview(responseMessage)
    print("Resultado " + responseMessage)
    st.session_state["messages2"].append({"role": "assistant", "content": "After analyzing the interview, I summarized the candidate's strengths and weaknesses as follows:"})
    st.session_state["messages2"].append({"role": "assistant", "content": responseMessage})
    store_qualifications(responseMessage)


def extract_qualifications(text):
    #text = 'Smart: High\nThoughtful: High\nOpen: Medium\nAdaptable: Medium\nTrusted: Low'
    lines = text.split('\n')
    values = []
    qualifications = []

    for line in lines:
        try:
            
            value, qualification = line.split(': ')
            value = re.sub(r'[^A-Z:a-z0-9]+', '', value.strip().lower())
            qualification = qualification.strip().lower() 
            
            if value in ['smart', 'thoughtful', 'open', 'adaptable', 'trusted']:
                values.append(value)
                qualifications.append(qualification)

        except Exception as e:
            print("Error method extract_qualifications " + str(e))

    return values, qualifications


def show_data(values, qualifications):

    qualifications[0] = 'low'
    datos = {
        'CompanyValue': values,
        'Level': qualifications
    }

    # print(datos)

    df = pd.DataFrame(datos)

    order_x = ['low', 'medium', 'high']
    df['Level'] = df['Level'].map({'low': 0, 'medium': 1, 'high': 2})
    df = df.sort_values(by='Level')
    df['Level'] = df['Level'].map({0: 'low', 1: 'medium', 2: 'high'})

    # Configurar el título de la aplicación
    st.title('Level of Company Values')

    # Crear un gráfico de barras utilizando matplotlib
    plt.figure(figsize=(10, 6))
    plt.barh(df['CompanyValue'], df['Level'], color='skyblue')
    plt.xlabel('Level')
    plt.ylabel('CompanyValue')
    plt.title('Level of Company Values')
    plt.grid(axis='x')

    # Establecer el orden de las etiquetas del eje x
    plt.xticks(ticks=[0, 1, 2], labels=order_x)

    # Mostrar el gráfico utilizando Streamlit
    st.pyplot(plt) 


def store_qualifications(response):

    global final_values
    global final_qualifications

    id = 0
    ids = []
    documents = []
    metadatas = []

    (values, qualifications) = extract_qualifications(response)
    final_values = values
    final_qualifications = qualifications

    print("Values:", values)
    print("Qualifications:", qualifications)

    for index in range(len(values)):

        value = values[index]

        id += 1
        ids.append("id"+ str(id))

        document = f"{value}: {qualifications[index]}"
        documents.append(document)

        source = {}
        source["source"] = value
        metadatas.append(source)        


    #print("ids:", ids)
    #print("metadatas:", metadatas)
    #print("documents:", documents)

    collection = store_collection(ids, metadatas, documents)
    st.chat_message("assistant").write(f"The next grapich show the results!!")




def store_collection (ids, metadatas, documents):
    try:
        client_database = connect_database()

        collection_name = "qualifications_candidate"
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




if __name__ == "__main__":

    if st.button('Clean Chat'):
        initalize_chat()

    menu_info.menu_messages()
    interview()

    show_data(final_values, final_qualifications)
