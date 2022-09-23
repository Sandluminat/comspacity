from pydantic import BaseSettings
import os

# Set language: "" means all languages
class Language():
    lang = ""

# pydantic: Input variable
class Input_variables():
    content = os.environ.get("content", "content")

class English():
    word_length = os.environ.get("word_length", 12)
    sentence_length = os.environ.get("sentence_length", 2)
    average_verbes = os.environ.get("average_verbes", 7)
    average_hard_words = os.environ.get("average_hard_words", 10)

class German():
    word_length = os.environ.get("word_length", 11)
    sentence_length = os.environ.get("sentence_length", 2)
    average_verbes = os.environ.get("average_verbes", 7)
