import streamlit as st
import pandas as pd
import menu_info
import chromadb
import re
from chromadb.config import Settings

#Config Page
st.set_page_config(
    page_title="Dashboard Candidates",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# show slidebar messages
menu_info.menu_messages()

data = {"name":[], "Rate":[]}

# connect database
def connect_database():
    client_database = chromadb.PersistentClient(path="./database/", settings=Settings(allow_reset=True))
    return client_database

client_database = connect_database()

def write_into_database():
    collection = client_database.get_or_create_collection(name="candidate_rating")
    collection.add(
            documents=["name: Dan rating: 8.5",
                       "name: Pedro rating: 7.5",
                       "name: Carlos Rodriguez rating: 6.5",
                       "name: Eric rating: 3.5",
                       "name: Gabriel Peralta rating: 9.5",
                       "name: Ignacio rating: 1.5"
                        ],
             ids= ["id1", "id2", "id4", "id5", "id6", "id7"]
        )
    
def get_candidate_data(collection):
    for document in collection.get()["documents"]:
        try:
            
            data["name"].append(re.search('name:(.*)rating:', document).group(1).strip())
            data["Rate"].append(float(re.search('rating:(.*)', document).group(1).strip()))
            
        except Exception as e:
            print("Error " + str(e) + " no actions")


    
def show_data():
    # client_database.reset()
    collection = client_database.get_or_create_collection(name="candidate_rating")
    if collection.count() <= 0:
        write_into_database()

    get_candidate_data(collection)
    dataframe = pd.DataFrame(data)
    dataframe = dataframe.set_index("name")

    st.bar_chart(dataframe)
    


show_data()


