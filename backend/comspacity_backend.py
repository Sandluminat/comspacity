import spacy
import json
import config
from fastapi import FastAPI
from pydantic import BaseModel, Field, Extra

# Load configs
e_weights = config.English()
g_weights = config.German()
input_variab = config.Input_variables()

# create BaseModel
class Text(BaseModel):
    texts: str = Field(alias=input_variab.content)

    class Config:
        allow_population_by_field_name = True
        extra=Extra.allow

app = FastAPI()

# Definitions
def set_language(lang, text):
    if lang == "english":
        nlp = spacy.load("en_core_web_sm")
    elif lang == "german":
        nlp = spacy.load("de_core_news_sm")
    doc = nlp(text)
    return doc

def reset_variables():
    words = 0
    words_length = 0
    verbes = 0
    hard_words = 0
    return words, words_length, verbes, hard_words

def get_complexity(lang, words, words_length, hard_words, words_per_sentence, verbes_per_sentence):
    average_word_length = words_length/words
    average_hard_words = hard_words/words

    if lang == "english":
        complexity_of_text = words_per_sentence*e_weights.sentence_length + verbes_per_sentence*e_weights.average_verbes + average_word_length*e_weights.word_length + average_hard_words*e_weights.average_hard_words 
    elif lang == "german":
        complexity_of_text = words_per_sentence*g_weights.sentence_length + verbes_per_sentence*g_weights.average_verbes + average_word_length*g_weights.word_length
    return complexity_of_text

def counting(token, json_object, words, words_length, verbes, hard_words):
    if spacy.explain(token.pos_) != "punctuation" and token.lemma_ != " " and "http" not in token.lemma_:
        words += 1
        words_length += len(token)

        if token.pos_ == "VERB":
            verbes += 1
        
        if token.text in json_object:
            pass
        else:
            hard_words += 1
    return words, words_length, verbes, hard_words

# API
@app.get("/ping")
def read_root():
    return {"pong"}

@app.post("/complexity/document/{language}")
async def create_item(txt: Text, language: str):
    text = txt.texts

    doc = set_language(language, text)

    words, words_length, verbes, hard_words = reset_variables()
    sentences = 1

    with open('sample.json', 'r') as openfile:
        json_object = json.load(openfile)
    
    for line in doc.sents:
        for token in line:
            words, words_length, verbes, hard_words = counting(token, json_object, words, words_length, verbes, hard_words)

            if spacy.explain(token.tag_) == "punctuation mark, sentence closer" or spacy.explain(token.tag_) == "sentence-final punctuation mark":
                sentences += 1
    
    # Can't put it in get_complexity function because the same function is used with complexity of sentences which doesn't use sentences.
    if sentences > 1:
        sentences-=1
    
    verbes_per_sentence = verbes/sentences
    words_per_sentence = words/sentences

    complexity_of_text = get_complexity(language, words, words_length, hard_words, words_per_sentence, verbes_per_sentence)  
    
    output = {
        "content": txt.texts,
        "complexityscore": complexity_of_text,
        }

    return output

@app.post("/complexity/sentences/{language}")
async def create_item(txt: Text, language: str):
    text = txt.texts

    doc = set_language(language, text)
    sentences_list = []

    with open('sample.json', 'r') as openfile:
        json_object = json.load(openfile)

    for line in doc.sents:
        sentence = line.text
        words, words_length, verbes, hard_words = reset_variables()

        for token in line:
            words, words_length, verbes, hard_words = counting(token, json_object, words, words_length, verbes, hard_words)
                    
            if spacy.explain(token.tag_) == "punctuation mark, sentence closer" or spacy.explain(token.tag_) == "sentence-final punctuation mark":
                complexity_of_sentence = get_complexity(language, words, words_length, hard_words, words, verbes)  
                sentences_list.append([sentence, complexity_of_sentence])

    sentences_list.sort(key = lambda x: -x[1])
    complexity_json = {sentences_list[i][0]: sentences_list[i][1] for i in range(len(sentences_list))}

    return complexity_json
