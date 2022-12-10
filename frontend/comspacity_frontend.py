import streamlit as st
import requests

endpoint = 'http://backend:8000/complexity/'

st.title("comspacity")
highlight_content = ""

language = st.selectbox("Choose your language", ("english", "german"))
type_of_complexity = st.selectbox("Do you want to know the complexity of a document or do you want to list the complexity of each phrase.", ("document", "sentences"))

sorted_sentences = []
new_list = []

txt = st.text_area("Enter your "+language+" text here.", height=300, max_chars=None)
if txt == "":
    pass
else:
    path=endpoint+type_of_complexity+"/"+language
    output = requests.post(path, json = {"texts": txt})
    if type_of_complexity == "sentences":
        out = output.json()
        sentences = out["sentence_complexity"]

        for i in sentences:
            sorted_sentences.append([i, sentences[i]])
        sorted_sentences.sort(key = lambda x: -x[1])
        y = int(len(sorted_sentences)*0.4) # Only the top 20% in the sense of complexity will be displayed
        if y == 0:
            y+=1
        sorted_sentences = sorted_sentences[0:y]
        for i in sorted_sentences:
            new_list.append(i[0])
        
        for i in sentences:
            if (i in new_list):
                x = (f" **{i.strip()}** ")
                highlight_content += x
            else:
               highlight_content += f"{i} "
        # st.write(out)
        st.write(highlight_content)
    else:    
        st.write(output.json())
