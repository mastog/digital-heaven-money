import configparser
import os

from backend.config import basedir


def load_word_mappings():
    # Load English and Chinese word mappings from the configuration file

    config = configparser.ConfigParser()
    config_path = os.path.join(basedir,"services", "words.ini")
    config.read(config_path, encoding="utf-8")
    word_mappings = config["Translations"]
    return word_mappings

def replace_words_list(text_list):
    # Replace English words with Chinese words in a list
    word_mappings=load_word_mappings()
    for i in range(len(text_list)):
        if text_list[i] in word_mappings:
            text_list[i] = word_mappings[text_list[i]]
    return text_list

def replace_words(text):
    # Replace English words with Chinese words in a text
    word_mappings = load_word_mappings()
    for chn_word, eng_word in word_mappings.items():
        text = text.replace(chn_word, eng_word)
    return text