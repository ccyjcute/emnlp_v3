# data_process.py
# modify 26
import json
import numpy as np
# from sentence_transformers import SentenceTransformer
import pickle
import faiss


############################
## Data process functions ##

def load_json(json_file):
    with open(json_file) as f:
        return json.load(f)


# def save_data(embeddings, words, embeddings_filename, words_filename):
#     with open(embeddings_filename, 'wb') as f:
#         pickle.dump(embeddings, f)

#     with open(words_filename, 'w') as f:
#         json.dump(words, f)

def read_text_file(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        return file.read()

############################







## not in use ###
def replace_phrase_in_text(original_text, old_phrase, new_phrase):
    return original_text.replace(old_phrase, new_phrase)