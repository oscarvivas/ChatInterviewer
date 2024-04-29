import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

import time
from dotenv import load_dotenv
from openai import AzureOpenAI

# Configure the client for Azure
client = AzureOpenAI (
    api_key="f78763df753c4c469a354c3a39ef6d14",
    azure_endpoint="https://aihackathoneastcan.openai.azure.com",
    api_version="2023-07-01-preview" # Ensure you use the correct API version
)

def ask_question (question):
    try:
        # Make an API call to the ChatCompletion model
        response = client.chat.completions.create(
            model="gpt-35-turbo-0613", # Ensure the engine name is correct for your setup 
            messages=[
                {"role": "system", "content": "Asistent is a large language model trained by openAI."}, 
                {"role": "user", "content": question }
            ]
        )    
        # Extract the message content from the response
        answer = response.choices[0].message.content
        return answer
    except Exception as e:
        return str(e) # Return the exception as a string for debugging
    
# Example usage of the function
if __name__ == "__main__":
    question = "hola"
    answer = ask_question (question)
    print("Question:", question)
    print("Answer:", answer)

