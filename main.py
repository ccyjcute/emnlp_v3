# __init__.py
# modify 6, 7, 62
from data_process import load_json, read_text_file #save_data, 
from prompt_engineer import extract_functional_language, generate_text_with_llm_few_shot, count_sentences_with_llm, check_sentence_count, cut_generated_article, remove_double_brackets
# from RAG import generate_RAG_data, semantic_search
import streamlit as st
from demo import update_status

import json
import numpy as np
import pickle
import faiss

def main(user_text_file):

    ####### Generate RAG data set ##########
    # generate_RAG_data()


    ############################################
    ####### Load embeddings from file ##########
    # with open('./RAG_data_base/embeddings_spoken.pkl', 'rb') as f:
    #     embeddings = pickle.load(f)
    # embeddings = {key: np.array(value) for key, value in embeddings.items()}  # convert lists back to numpy arrays
    
    # # Load words from file
    # with open('./RAG_data_base/words_spoken.json', 'r') as f:
    #     words = json.load(f)
    
    # # Create FAISS index for each group of words
    # indices = {key: faiss.IndexFlatL2(value.shape[1]) for key, value in embeddings.items()}
    
    # # Add embeddings to their respective FAISS index
    # for key, index in indices.items():
    #     index.add(embeddings[key])
    ##############################################
    ##############################################
    

    # Read user text
    user_text = read_text_file(user_text_file)
    print(f"User text: {user_text}")




    ###################################################
    # 1. Check if the input text meet the length limit
    ###################################################

    sentence_count = count_sentences_with_llm(user_text)
    # print(sentence_count)

    ###############################################
    # 2. Generate modified text
    ###############################################
    
    if check_sentence_count(sentence_count):
        modify_text = generate_text_with_llm_few_shot(user_text)  
    else:
        # raise ValueError("The input text does not meet the length limit.")
        update_status(":red[Limited to a maximum of 20 sentences!]", "error")

    clean_modify_text = remove_double_brackets(modify_text)


    ###############################################
    # 3. Extracting functional language from the generate text
    ###############################################

    
    extract_sentence = extract_functional_language(clean_modify_text)   
        
    target_phrases = []
    functional_type = []
    original_sentences = []

    # print(f"Extracted functional language: {extract_sentece}")
    for sentence in extract_sentence:
        print(sentence)
        original_sentences.append(sentence.split('|')[2].strip())
        target_phrases.append(sentence.split('|')[3].strip())
        functional_type.append(sentence.split('|')[4].strip())
    
    # print(f"Extracted functional language: {target_phrases}")
    # print(f"Extracted functional language type: {functional_type}")
    ##################################################
    

    #####################################################
    

    return clean_modify_text, extract_sentence





# Example usage (replace the paths with actual file paths)
if __name__ == "__main__":
    
    ######
    # TODO 
    # Let user choose a default script
    default_script = "student_01" # student_02, lecturer_01, lecturer_02
    ######


    # define input/output directory
    input_directory = "./test_data/Default_original_input"
    output_directory = "./test_data/Default_modified_output"
    

    user_text_file = f"{input_directory}/{default_script}.txt"
    

    # TODO
    # The ouput of the system
    # generated_text: the modify text generate by the system
    # generate_text_extract_table: the table contain extracted lexical bundles of the generated text 
    generate_script, generate_text_extract_table = main(user_text_file)



    ###############################
    # Write the output to the file
    with open(f"{output_directory}/{default_script}_modified.txt", 'w') as f:
        f.write(generate_script)


    with open(f"{output_directory}/{default_script}_extract_modified_table.txt", 'w') as f:

        f.write("| Sentence Number | Sentence | Phrase | Rhetorical Function |\n")
        f.write("| -------------- | -------- | -------- | -------------------- |\n")

        for line in generate_text_extract_table:
            f.write(line+"\n")


    print("------------------------------")
    print("-----System process over------")
    print("------------------------------")