import streamlit as st
import requests

endpoint = 'http://127.0.0.1:8000/complexity/'

st.title("Comspacity")

txt = st.text_area("I want your knowledge...", height=300, max_chars=None)
if txt == "":
    pass
else:
    path=endpoint
    output = requests.post(path, json = {"texts": txt})
    st.write(output.json())