import streamlit as st
import os

#Config Page
st.set_page_config(
    page_title="Uploader Profiles",
    page_icon="outbox_tray"
)

profiles_path = os.getenv("PROFILES_PATH")

uploaded_files = st.file_uploader("**Choose profiles (PDF files) to upload** :page_with_curl:", type="PDF", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    with open(os.path.join(profiles_path, uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.write("Saved filename:", uploaded_file.name)
    # st.success("Saved file:", uploaded_file.name)
    # st.write(bytes_data)
    



