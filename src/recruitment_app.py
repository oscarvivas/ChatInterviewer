# libraries to import
from openai import AzureOpenAI
from dotenv import load_dotenv
import os
import streamlit as st

# load environment vars
load_dotenv()

# create a openai client
client = AzureOpenAI (
    api_key=os.getenv("OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    api_version=os.getenv("API_VERSION") # Ensure you use the correct API version
)

prompt = """You are an expert recruiter who evaluates the strengths and weaknesses of a candidate for a Frontend developer position.
            Your job is to ask the candidate a series of questions to identify and evaluate his or her strengths and weaknesses. You should ask for as much detail as you need.
            Thought process:
                [Step 1]: Tell me about a time when you faced a challenge and how you handled it.
                [Step 2]: Identify your strengths with the previous answer
                [Step 3]: Calculate the level of expertise of these strengths with a numerical value from 1 to 5.
                [Step 4]: Generate a table with the following structure [strength, rating]
                [Step 5]: Identify weaknesses with the answer from step 1
                [Step 7]: Generate a table with the following structure [weakness]
            When the user starts the conversation, you should introduce yourself in a friendly way."""

def menu():
    st.title("💬 Chat Interviewer")

    st.sidebar.subheader("About")
    st.sidebar.markdown("This is a chat interviewing application.")

    st.sidebar.subheader("Instructions")
    st.sidebar.markdown("Answer the questions asked by the interviewer using the chat interface.")

    st.sidebar.subheader("About Me")
    st.sidebar.markdown("I am an AI-powered interviewer, ready to ask you questions!")


def interview():
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "system", "content": prompt}]
        #st.session_state["messages"] = [{"role": "assistant", "content": "Hello, I'm a recruitment assistant! How can I help you?"}]

    for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).write(msg["content"])

    user_input = st.chat_input()
    if user_input:
        st.session_state["messages"].append({"role": "user", "content": user_input })
        st.chat_message("user").write(user_input)
    
    responseMessage = ask_openai(st.session_state["messages"])
    st.session_state["messages"].append({"role": "system", "content": responseMessage})


def ask_openai (chatMessages):
    try:
        # Make an API call to the ChatCompletion model
        response = client.chat.completions.create(
            model="gpt-35-turbo-0613", # Ensure the engine name is correct for your setup 
            messages=chatMessages
        )    
        # Extract the message content from the response
        answer = response.choices[0].message.content
        return answer
    except Exception as e:
        return str(e) # Return the exception as a string for debugging 


if __name__ == "__main__":

    menu()
    interview()
