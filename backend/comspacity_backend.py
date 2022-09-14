import spacy
import json
from fastapi import FastAPI
from pydantic import BaseModel

class Text(BaseModel):
    texts: str

app = FastAPI()

@app.get("/ping")
def read_root():
    return {"pong"}

@app.post("/complexity/document/{language}")
async def create_item(txt: Text, language: str):
    text = txt.texts

    # language distinction 1
    if language == "english":
        nlp = spacy.load("en_core_web_sm")
    elif language == "german":
        nlp = spacy.load("de_core_news_sm")
    doc = nlp(text)

    sentences = 0
    words = 0
    words_length = 0
    verbes = 0
    with open('sample.json', 'r') as openfile:
        json_object = json.load(openfile)
    hard_words = 0

    for line in doc.sents:
        for token in line:
            # passives
            if spacy.explain(token.pos_) != "punctuation" and token.lemma_ != " " and "http" not in token.lemma_:
                words += 1
                words_length += len(token)

                if token.pos_ == "VERB":
                    verbes += 1
                
                if token.text in json_object:
                    pass
                else:
                    hard_words += 1


            if spacy.explain(token.tag_) == "punctuation mark, sentence closer" or spacy.explain(token.tag_) == "sentence-final punctuation mark":
                sentences += 1
    
    average_word_length = words_length/words
    words_per_sentence = words/sentences
    average_hard_words = hard_words/words
    verbes_per_sentence = verbes/sentences

    # language distinction 2
    if language == "english":
        complexity_of_text = words_per_sentence/17.5*35 + verbes_per_sentence/1.5*10 + average_word_length/4.7*55 + average_hard_words*10 
    elif language == "german":
        complexity_of_text = words_per_sentence/17.5*38 + verbes_per_sentence/1.5*12 + average_word_length/5*60
    
    output = {
        "average hard words": average_hard_words,
        "content": txt.texts,
        "complexityscore": complexity_of_text,
        }

    return output

@app.post("/complexity/sentences/{language}")
async def create_item(txt: Text, language: str):
    text = txt.texts

    # Language distinction 1
    if language == "english":
        nlp = spacy.load("en_core_web_sm")
    elif language == "german":
        nlp = spacy.load("de_core_news_sm")
    doc = nlp(text)

    with open('sample.json', 'r') as openfile:
        json_object = json.load(openfile)
    sentences = []

    for line in doc.sents:
        sentence = line.text
        words = 1
        words_length = 0
        verbes = 0
        hard_words = 0

        for token in line:
            # passives
            if spacy.explain(token.pos_) != "punctuation" and token.lemma_ != " ":
                if "http" in token.text:
                    words += 1
                else:
                    words += 1
                    words_length += len(token)
                    if token.pos_ == "VERB":
                        verbes += 1

                    if token.text in json_object:
                        pass
                    else:
                        hard_words += 1
                    
            if spacy.explain(token.tag_) == "punctuation mark, sentence closer" or spacy.explain(token.tag_) == "sentence-final punctuation mark":
                average_word_length = words_length/words
                average_hard_words = hard_words/words


                # Language distinction 2.
                if language == "english":
                    complexity_of_sentence = words/17.5*38 + verbes/1.5*12 + average_word_length/4.7*60 + average_hard_words*100
                elif language == "german":
                    complexity_of_sentence = words/17.5*38 + verbes/1.5*12 + average_word_length/5*60
                
                sentences.append([sentence, complexity_of_sentence])
                words = 1
                words_length = 0
                verbes = 0
                hard_words = 0

    sentences.sort(key = lambda x: -x[1])
    complexity_json = {sentences[i][0]: sentences[i][1] for i in range(len(sentences))}

    return complexity_json
