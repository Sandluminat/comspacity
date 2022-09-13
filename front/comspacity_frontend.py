import streamlit as st
import requests

endpoint = 'http://backend:8000/complexity/'

st.title("Comspacity")

language = st.selectbox("Choose your language", ("english", "german"))
type_of_complexity = st.selectbox("Do you want to know the complexity of a document or do you want to list the complexity of each phrase.", ("document", "sentences"))

txt = st.text_area("Enter your "+language+" text here.", height=300, max_chars=None)
if txt == "":
    pass
else:
    path=endpoint+type_of_complexity+"/"+language
    output = requests.post(path, json = {"texts": txt})
    st.write(output.json())