import json
import numpy as np
# from sentence_transformers import SentenceTransformer
import pickle
import faiss


from data_process import load_json, save_data



def generate_RAG_data():

    json_file = './RAG_data_base/lexical_bundle_taxonomy.json'
    data = load_json(json_file)
    
    # Generate embeddings and words
    embeddings, words = generate_embeddings(data)
    
    # Save embeddings and words to files
    save_data(embeddings, words, './RAG_data_base/embeddings_spoken.pkl', './RAG_data_base/words_spoken.json')
    


############################
########    RAG  ###########

# def generate_embeddings(data, model_name='all-MiniLM-L6-v2'):
#     model = SentenceTransformer(model_name)
#     embeddings = {}
#     words = {}
#     for key, word_list in data.items():
#         # print(key)
#         embeddings[key] = model.encode(word_list).tolist()  # convert numpy array to list
#         words[key] = word_list
#     return embeddings, words


# def semantic_search(query, key, sent ,indices, words, model_name='all-MiniLM-L6-v2', top_k=1):
#     model = SentenceTransformer(model_name)
#     query_embedding = model.encode([query])
#     sent_embedding = model.encode([sent])
#     faiss.normalize_L2(query_embedding+sent_embedding)  # Normalize query for cosine similarity
#     results = []
#     if key in indices:
#         index = indices[key]  # Select the correct FAISS index for search
#         distances, search_indices = index.search(query_embedding, top_k)
#         results = [words[key][idx] for idx in search_indices[0]]  # Select corresponding words
#     return results

#############################