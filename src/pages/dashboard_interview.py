import streamlit as st
import pandas as pd
import menu_info

#Config Page
st.set_page_config(
    page_title="Dashboard Interview",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# show slidebar messages
menu_info.menu_messages()


data = {"name":["Peter","Dan","Carlos","Cesar","Sergio"], "Rate":[2300,2510,1121,900,8456]}
data = pd.DataFrame(data)
data = data.set_index("name")

#st.write(data)
st.bar_chart(data)
