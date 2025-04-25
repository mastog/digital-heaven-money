import configparser
import os

from backend.config import basedir


def load_word_mappings():
    # Load English and Chinese word mappings from the configuration file
    config = configparser.ConfigParser()
    config_path = os.path.join(basedir, "services", "words.ini")
    config.read(config_path, encoding="utf-8")
    return config["Translations"]


def replace_words_list(text_list):

    word_mappings = load_word_mappings()
    # first five
    limit = min(5, len(text_list))
    new_list=[]
    for i in range(limit):
        original_word = text_list[i]
        if original_word in word_mappings:
            new_list.append(word_mappings[original_word])
    return new_list


def replace_words(text):

    word_mappings = load_word_mappings()
    for eng_word, chn_word in word_mappings.items():
        text = text.replace(eng_word, chn_word)
    return text