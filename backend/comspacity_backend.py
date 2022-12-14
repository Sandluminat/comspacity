import spacy
import json
import config
from fastapi import FastAPI
from pydantic import BaseModel, Field, Extra

# Load configs
e_weights = config.English()
g_weights = config.German()
input_variab = config.Input_variables()

lang = config.Language.lang
if lang == "":
    nlp_english = spacy.load("en_core_web_sm")
    nlp_german = spacy.load("de_core_news_sm")
elif lang == "english":
    nlp_english = spacy.load("en_core_web_sm")
elif lang == "german":
    nlp_german = spacy.load("de_core_news_sm")


# create BaseModel
class Text(BaseModel):
    texts: str = Field(alias=input_variab.content)
    complexityscore: float = Field(default=0.0)

    class Config:
        allow_population_by_field_name = True
        extra=Extra.allow

class Text_sentences(BaseModel):
    texts: str = Field(alias=input_variab.content)
    sentence_complexity: dict = Field(default={"no": "sentences"})

    class Config:
        allow_population_by_field_name = True
        extra=Extra.allow

app = FastAPI()

# Definitions
def set_language(lang, text):
    if lang == "english":
        nlp = nlp_english
    elif lang == "german":
        nlp = nlp_german
    doc = nlp(text)
    return doc

def reset_variables():
    words = 0
    words_length = 0
    verbes = 0
    hard_words = 0
    return words, words_length, verbes, hard_words

def get_complexity(lang, words, words_length, hard_words, words_per_sentence, verbes_per_sentence):
    try:    
        average_word_length = words_length/words
        average_hard_words = hard_words/words
    except:
        average_word_length = 0
        average_hard_words = 0
    if hard_words == 0:
        average_hard_words = 0

    if lang == "english":
        complexity_of_text = words_per_sentence*e_weights.sentence_length + verbes_per_sentence*e_weights.average_verbes + average_word_length*e_weights.word_length + average_hard_words*e_weights.average_hard_words 
    elif lang == "german":
        complexity_of_text = words_per_sentence*g_weights.sentence_length + verbes_per_sentence*g_weights.average_verbes + average_word_length*g_weights.word_length
    
    if complexity_of_text < 0:
        complexity_of_text = 0
    return complexity_of_text

def counting(token, json_object, words, words_length, verbes, hard_words):
    if spacy.explain(token.pos_) != "punctuation" and token.lemma_ != " " and "http" not in token.lemma_:
        words += 1
        words_length += len(token)

        if token.pos_ == "VERB":
            verbes += 1

        if token.lower_ in json_object:
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
    sentences = 0

    with open('sample.json', 'r') as openfile:
        json_object = json.load(openfile)

    for line in doc.sents:
        for token in line:
            words, words_length, verbes, hard_words = counting(token, json_object, words, words_length, verbes, hard_words)

        sentences += 1

    try:
        verbes_per_sentence = verbes/sentences
        words_per_sentence = words/sentences
    except:
        verbes_per_sentence = 0
        words_per_sentence = 0

    complexity_of_text = get_complexity(language, words, words_length, hard_words, words_per_sentence, verbes_per_sentence)  

    txt.complexityscore=complexity_of_text

    return txt

@app.post("/complexity/sentences/{language}")
async def create_item(txt: Text_sentences, language: str):
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
                    
        complexity_of_sentence = get_complexity(language, words, words_length, hard_words, words, verbes)  
        sentences_list.append([sentence, complexity_of_sentence])

    #??sentences_list.sort(key = lambda x: -x[1]) # If you want a sorted sentence list.
    complexity_json = {sentences_list[i][0]: sentences_list[i][1] for i in range(len(sentences_list))}
    txt.sentence_complexity = complexity_json

    return txt
