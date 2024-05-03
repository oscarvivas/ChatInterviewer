# libraries to import
from openai import AzureOpenAI
from dotenv import load_dotenv
import os
import streamlit as st
import menu_info
import azure.cognitiveservices.speech as speechsdk


def transcribe_audio(speech_config):
    audio_config = speechsdk.AudioConfig(use_default_microphone=False)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    result = speech_recognizer.recognize_once_async().get()
    return result.text.strip()

speech_config = speechsdk.SpeechConfig(subscription="d9e4e91e17aa4fc7a2ebcefc71058b05", region="eastus")
synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)


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

prompt = """You are an expert recruiter and your name is HADA, who evaluates the strengths and weaknesses of a candidate for a Frontend developer position.
            Your job is to ask the candidate a series of questions to identify and evaluate his or her strengths and weaknesses. You should ask for as much detail as you need.
            Chain of Thought:
                [Step 1]: Tell me about a time when you faced a challenge and how you handled it.
                [Step 2]: Identify your strengths with the previous answer
                [Step 3]: Calculate the level of expertise of these strengths with a numerical value from 1 to 5.
                [Step 4]: Generate a table with the following structure [strength, rating]
                [Step 5]: Identify weaknesses with the answer from step 1
                [Step 7]: Generate a table with the following structure [weakness]
            When the user starts the conversation, you should introduce yourself in a friendly way. and no more than 3 question.
            This is your only role."""

def interview():
    speech_config = speechsdk.SpeechConfig(subscription="d9e4e91e17aa4fc7a2ebcefc71058b05", region="eastus")
    if "messages2" not in st.session_state:
        # Init the ChatCompletion model with the prompt
        responseMessage = ask_openai([{"role": "system", "content": prompt}])
        st.session_state["messages2"] = [{"role": "system", "content": responseMessage}]
        synthesize_and_save_speech(speech_config,responseMessage)
        #st.session_state["messages2"] = [{"role": "system", "content": prompt}] 

    user_input = st.chat_input()
    if user_input: 
        st.session_state["messages2"].append({"role": "user", "content": user_input }) 
        #st.chat_message("user").write(user_input)      -- Self interview
        responseMessage = ask_openai(st.session_state["messages2"])
        st.session_state["messages2"].append({"role": "system", "content": responseMessage})
        synthesize_and_save_speech(speech_config,responseMessage)
        
    for msg in st.session_state["messages2"]:
        st.chat_message(msg["role"]).write(msg["content"])
        #if msg["role"] == "system":
        #  synthesize_and_save_speech(speech_config,msg["content"])

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

def synthesize_and_save_speech(speech_config, responseMessage):
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    speech_synthesizer.speak_text_async(responseMessage).get()
    

if __name__ == "__main__":

    menu_info.menu_messages()
    interview()
