import streamlit as st
import pandas as pd
import menu_info
import plotly.express as px
import chromadb
import re
from chromadb.config import Settings

#Config Page
st.set_page_config(
    page_title="Dashboard Interview",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# show slidebar messages
menu_info.menu_messages()


# Title
st.title('Interview results')

data = {"EndavaValue":[], "Weighing":[]}

# connect database
def connect_database():
    client_database = chromadb.PersistentClient(path="./database/", settings=Settings(allow_reset=True))
    return client_database

client_database = connect_database()

def write_into_database():
    collection = client_database.get_or_create_collection(name="qualifications_candidate")
    collection.add(
            documents=["Smart: Low",
                       "Thoughtful: High",
                       "Open: High",
                       "Adaptable: Medium",
                       "Trusted: Medium"
                        ],
             ids= ["id1", "id2", "id4", "id5", "id6"]
        )
    
def get_qualifications_data(collection):
    for document in collection.get()["documents"]:
        try:
            parts = document.split(" ")
            value = parts[0].replace(":", "")
            rating = parts[1]
            data["Weighing"].append(rating)
            data["EndavaValue"].append(value)
            
        except Exception as e:
            print("Error " + str(e) + " no actions")


    
def show_data():
    # client_database.reset()
    collection = client_database.get_or_create_collection(name="qualifications_candidate")
    if collection.count() <= 0:
        write_into_database()

    get_qualifications_data(collection)
    df = pd.DataFrame(data)

    fig = px.bar(df, x='Weighing', y='EndavaValue', orientation='h',  color='Weighing', 
                color_continuous_scale=px.colors.sequential.Viridis, labels={'Weighing': 'Weighing scale'})

    # Setting up
    fig.update_layout(xaxis_title='Weighing', yaxis_title='Endava Values',
                    font=dict(family="Arial", size=12, color="black"),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)')

    # set range
    values_range = ['Low', 'Medium', 'High']

    # Update the x range
    fig.update_xaxes(categoryorder='array', categoryarray=values_range)

    # Show the grafic 
    st.plotly_chart(fig)
    


show_data()





