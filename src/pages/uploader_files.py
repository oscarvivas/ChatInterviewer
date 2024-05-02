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
    


# image_file = st.file_uploader("Upload An Image",type=['png','jpeg','jpg'])
# if image_file is not None:
#     file_details = {"FileName":image_file.name,"FileType":image_file.type}
#     st.write(file_details)
#     img = self.upload_file(image_file)
#     st.image(img,height=250,width=250)
#     with open(os.path.join("tempDir",image_file.name),"wb") as f: 
#       f.write(image_file.getbuffer())         
#     st.success("Saved File")
