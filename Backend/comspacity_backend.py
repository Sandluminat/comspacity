import spacy
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
    word_list_frequency = []
    word_list_test =[]
    words_length = 0
    verbes = 0
    adjectives = 0

    for line in doc.sents:
        for token in line:
            # passives
            if spacy.explain(token.pos_) != "punctuation" and token.lemma_ != " " and "http" not in token.lemma_:
                words += 1
                words_length += len(token)

                if spacy.explain(token.pos_) == "adjective":
                    adjectives += 1
                elif token.pos_ == "VERB":
                    verbes += 1
                
                if token.lemma_ in word_list_test:
                    word_index = word_list_test.index(token.lemma_)
                    word_list_frequency[word_index][1] += 1

                else:
                    word_list_frequency.append([token.lemma_, 1])
                    word_list_test.append(token.lemma_)


            if spacy.explain(token.tag_) == "punctuation mark, sentence closer" or spacy.explain(token.tag_) == "sentence-final punctuation mark":
                sentences += 1
    
    average_word_length = words_length/words
    average_word_frequency = words/len(word_list_test)
    words_per_sentence = words/sentences
    verbes_per_sentence = verbes/sentences
    word_list_frequency.sort(key=lambda x: (-x[1]))

    # language distinction 2
    if language == "english":
        complexity_of_text = words_per_sentence/17.5*38 + verbes_per_sentence/1.5*12 + average_word_length/4.7*60 - average_word_frequency/3.5*10
    elif language == "german":
        complexity_of_text = words_per_sentence/17.5*38 + verbes_per_sentence/1.5*12 + average_word_length/5*60 - average_word_frequency/3.5*10

    return complexity_of_text, sentences, words, words_per_sentence, average_word_length, average_word_frequency, verbes_per_sentence, verbes, adjectives, word_list_frequency

@app.post("/complexity/sentences/{language}")
async def create_item(txt: Text, language: str):
    text = txt.texts

    # Language distinction 1
    if language == "english":
        nlp = spacy.load("en_core_web_sm")
    elif language == "german":
        nlp = spacy.load("de_core_news_sm")
    doc = nlp(text)

    words = 0
    words_length = 0
    verbes = 0
    adjectives = 0
    sentences = []

    for line in doc.sents:
        sentence = line.text
        for token in line:
            # passives
            if spacy.explain(token.pos_) != "punctuation" and token.lemma_ != " ":
                if "http" in token.text:
                    words += 1
                else:
                    words += 1
                    words_length += len(token)
                    if spacy.explain(token.pos_) == "adjective":
                        adjectives += 1
                    if token.pos_ == "VERB":
                        verbes += 1
            if spacy.explain(token.tag_) == "punctuation mark, sentence closer" or spacy.explain(token.tag_) == "sentence-final punctuation mark":
                average_word_length = words_length/words

                # Language distinction 2.
                if language == "english":
                    complexity_of_sentence = words/17.5*38 + verbes/1.5*12 + average_word_length/4.7*60
                elif language == "german":
                    complexity_of_sentence = words/17.5*38 + verbes/1.5*12 + average_word_length/5*60
                
                sentences.append([sentence, complexity_of_sentence, words, average_word_length, verbes, adjectives])
                words = 0
                words_length = 0
                verbes = 0
                adjectives = 0
    sentences.sort(key = lambda x: -x[1])   
    return sentences