import configparser

def load_word_mappings():
    # Load English and Chinese word mappings from the configuration file

    config = configparser.ConfigParser()
    config.read("words.ini", encoding="utf-8")
    word_mappings = config["Translations"]
    return word_mappings

def replace_words(text_list):
    # Replace English words with Chinese words in a data structure
    word_mappings=load_word_mappings()
    for i in range(len(text_list)):
        if text_list[i] in word_mappings:
            text_list[i] = word_mappings[text_list[i]]
    return text_list