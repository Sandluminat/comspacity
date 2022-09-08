import spacy
from fastapi import FastAPI
from pydantic import BaseModel

class Text(BaseModel):
    texts: str

app = FastAPI()

@app.get("/ping")
def read_root():
    return {"pong"}

@app.post("/complexity/{language}")
async def create_item(txt: Text, language: str):
    text = txt.texts
    if language == "english":
        nlp = spacy.load("en_core_web_sm")
    elif language == "german":
        nlp = spacy.load("de_core_news_sm")
    doc = nlp(text)
    doc = nlp(text)

    sentences = 0
    words = 0
    words_length = 0
    verbes = 0
    adjectives = 0

    for line in doc.sents:
        for token in line:
            print(spacy.explain(token.tag_))
            # passives & Wordfrequency
            if spacy.explain(token.pos_) != "punctuation":
                words += 1
                words_length += len(token)
            if spacy.explain(token.pos_) == "adjective":
                adjectives += 1
            if token.pos_ == "VERB":
                verbes += 1
            if spacy.explain(token.tag_) == "punctuation mark, sentence closer" or spacy.explain(token.tag_) == "sentence-final punctuation mark":
                sentences += 1
    
    average_word_length = words_length/words
    words_per_sentence = words/sentences
    complexity_of_text = words_per_sentence/17.5*38 + verbes/1.5*12 + average_word_length/4.7*60
    return complexity_of_text, sentences, words, words_per_sentence, average_word_length, verbes, adjectives
