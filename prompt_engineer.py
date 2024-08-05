# prompt_engineer.py
import streamlit as st
##############################################################
## This file is to define the function that calls opeai API ##
##############################################################



import openai
from data_process import read_text_file

openai.api_key = st.secrets["openai_key"]  # Replace with your OpenAI API key


#########################################
# The function to extract lexical bundles 
# Will return a table with 4 column

def extract_functional_language(text):
    system = read_text_file("./prompt/extract_lexical_bundles.txt")
    prompt = f"'{text}'"
    response = openai.ChatCompletion.create(
        model='gpt-4o',  # Use gpt-4 model
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1400,  # Adjust the max_tokens as needed
        temperature=0.8,  # Adjust the temperature as needed
        top_p=0.9,        # Adjust the top_p as needed
    )
    return response.choices[0].message['content'].strip().split('\n')[2:]  # Assuming the model lists phrases line by line



##############################################################################################
# The function is to generate full script with the lexical bundles retrieved from RAG database
# Will return a full script  

def generate_text_with_llm_few_shot(prompt, model='gpt-4o'):
    system = read_text_file("./prompt/EMI_script_genrate_1.txt")
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2000,  # Adjust the max_tokens as needed
        temperature=1.3,  # Adjust the temperature as needed
        top_p=0.9,        # Adjust the top_p as needed
    )
    return response.choices[0].message['content'].strip()


# def generate_text_with_llm(prompt, model='gpt-4-turbo'):
#     system = read_text_file("./prompt/generation_new_script.txt")
#     response = openai.ChatCompletion.create(
#         model=model,
#         messages=[
#             {"role": "system", "content": system},
#             {"role": "user", "content": prompt}
#         ],
#         max_tokens=4000  # Adjust the max_tokens as needed
#     )
#     return response.choices[0].message['content'].strip()



############################################################################
# The fucntion is to count how many senence in a given text
# The current system should not allow text more than 20 sentences. 

def count_sentences_with_llm(text, model='gpt-4o'):

    system = (
        "You will be given a user's text as input. Please count the number of sentences in the user's input text:\n"

        "The definition of a sentence: A sentence means a group of words that makes complete sense. It begins with a capital letter and ends with a full stop.\n"

        "Steps:\n"
        "1. Identify every sentence in the input text with the definition of a sentence.\n"
        "2. Use the Chain of Thoughts to count the sentences in the input text one by one.\n"
        "3. The count of the sentences is the total number of sentences of the text.\n"
        "3. Return the total number of sentences as the result.\n"

        "------------------------------------------\n"
        "Example:\n "

        "- Example User Input:\n"
        "Last time, we took a look at a game about choosing grades, emphasizing that outcomes alone aren't enough without payoffs. That is to say, payoffs become a normal-form game where Alpha strictly dominates Beta, teaching us to avoid strictly dominated strategies.\n \
        Today, we discussed the Prisoners' Dilemma with examples like joint projects and price competition, stressing the need for contracts, treaties, and regulations. You can see that essential game ingredients include players, strategies, and payoffs, illustrated with an example involving Player I and Player II. \n \
        Repeated interactions and learning are crucial. \n\
        Let's say players chose numbers from 1 to 100, aiming to get closest to two-thirds of the average. As shown in figure, choices moved from random to calculated, resulting different levels of reasoning. \n \
        One of the most important things is that common knowledge is critical, requiring understanding not just what we know, but what others know we know. A lot of times even mutual knowledge doesn't always mean common knowledge. \n \
        At the end of the class, it is important for you to remember that repeated gameplay and discussions enhance strategic thinking, shown by decreasing chosen numbers over time. Knowing rationality and layered knowledge helps players to adjust, in the sense of strategies, and will prepare for more complex games ahead. \n \
        Next week, don't forget you have to hand in your assignment two. I don't know why a lot of you failed to do this last week.Thank you very much. Class dismissed."
        

        "- Example Chain of Thoughts: Check every sentence from the input text one by one:\n"

        "Sentence 1: Last time, we took a look at a game about choosing grades, emphasizing that outcomes alone aren't enough without payoffs. "
        "Sentence 2: That is to say, payoffs become a normal-form game where Alpha strictly dominates Beta, teaching us to avoid strictly dominated strategies."
        "Sentence 3: Today, we will discuss the Prisoners' Dilemma with examples like joint projects and price competition, stressing the need for contracts, treaties, and regulations."  
        "Sentence 4: You can see that, essential game ingredients include players, strategies, and payoffs, illustrated with an example involving Player I and Player II."  
        "Sentence 5: Repeated interactions and learning are crucial."
        "Sentence 6: Players chose numbers from 1 to 100, aiming to get closest to two-thirds of the average."  
        "Sentence 7: As shown in figure, choices moved from random to calculated, resulting different levels of reasoning."  
        "Sentence 8: One of the most important things is that common knowledge is critical, requiring understanding not just what we know, but what others know we know."  
        "Sentence 9: A lot of times even mutual knowledge doesn't always mean common knowledge."  
        "Sentence 10: At the end of the class, it is important for you to remember that repeated gameplay and discussions enhance strategic thinking, shown by decreasing chosen numbers over time."  
        "Sentence 11: Knowing rationality and layered knowledge helps players to adjust, in the sense of strategies, and prepare for more complex games ahead.  "
        "Sentence 12: Next week, don't forget you have to hand in your assignment two."
        "Sentence 13: I don't know why a lot of you failed to do this last week."  
        "Sentence 14: Thank you very much."
        "Sentence 15: Class dismissed.\n"

        "There are 15 sentence in the example input text in total.\n"
        
        "- Example output:\n"
        "15\n"
        "------------------------------------------\n"

        "------------------------------------------\n"

        "You will be given a user's text as input." 
        "Please count the number of sentences in the user's input text with the steps above.\n"
        "**- Notice:** Return(output) ONLY the total number of sentences as result (integer) .\n"
        "**- Notice:** The ouput is an interger."
        "**- Notice:** Do not return or print anything else .\n"
    )

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": text}
        ],
        max_tokens=20  # Adjust the max_tokens as needed
    )

    result = response.choices[0].message['content'].strip()

    try:
        sentence_count = int(result)
    except ValueError:
        sentence_count = -1  # If parsing fails, return -1 as an error indicator.

    return sentence_count





#########################################################
# Some function process the result of the above functions
#########################################################


def check_sentence_count(user_input_count):
    if (user_input_count > 25):
        print("Input text exceeds limit!\nThe system accept text less than 20 sentences.")
        return 0
    return 1

def cut_generated_article(text):
    start_phrase = "--Complete Article:--"
    start_index = text.find(start_phrase)

    if start_index == -1:
        return "Complete Article not found in the text."

    complete_article_text = text[start_index + len(start_phrase):].strip()
    return complete_article_text

def remove_double_brackets(text):
    # Replace all occurrences of "[[" and "]]"
    cleaned_text = text.replace('[[', '').replace(']]', '')
    return cleaned_text