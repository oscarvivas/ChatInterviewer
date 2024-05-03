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

prompt = """Generate an interview between a Human Resources (HR) recruiter and a candidate for the .NET Developer position. The interview should address both technical and soft skills and contain a maximum of 10 questions and answers."""

def interview():
    if "messages2" not in st.session_state:
        # Init the ChatCompletion model with the prompt
        responseMessage = ask_openai([{"role": "system", "content": prompt}])
        st.session_state["messages2"] = [{"role": "system", "content": responseMessage}]
        #st.session_state["messages"] = [{"role": "system", "content": prompt}] 

    user_input = st.chat_input()
    if user_input: 
        st.session_state["messages2"].append({"role": "user", "content": user_input }) 
        #st.chat_message("user").write(user_input)      -- Self interview
        responseMessage = ask_openai(st.session_state["messages2"])
        st.session_state["messages2"].append({"role": "system", "content": responseMessage})
        
    for msg in st.session_state["messages2"]:
        st.chat_message(msg["role"]).write(msg["content"])

def ask_openai (chatMessages):
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
    

if __name__ == "__main__":

    menu_info.menu_messages()
    interview()
