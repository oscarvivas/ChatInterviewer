# libraries to import
from openai import AzureOpenAI
from dotenv import load_dotenv
import os
import streamlit as st
import menu_info

#Config Page
st.set_page_config(
    page_title="Recuitment Interview",
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
You should generate a table with the next format [Value, Rating]
You should use the next interview """

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
    responseMessage = generate_interview([{"role": "assistant", "content": prompt}])
    st.session_state["messages2"] = [{"role": "assistant", "content": responseMessage}]

    responseMessage = analize_interview(responseMessage)
    st.session_state["messages2"].append({"role": "assistant", "content": responseMessage})


if __name__ == "__main__":

    if st.button('Clean Chat'):
        initalize_chat()

    menu_info.menu_messages()
    interview()
