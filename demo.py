import streamlit as st
import pandas as pd
import numpy as np
import time
from main import *
import re

default_path = "./default.txt"

if "submission_status_text" not in st.session_state:
    st.session_state["submission_status_text"] = ":green[Ready to improve!]"
if "submission_status_icon" not in st.session_state:
    st.session_state["submission_status_icon"] = "complete"
if "lexicalBundleType" not in st.session_state:
    st.session_state["lexicalBundleType"] = "**Type:**"
if "lexicalBundleDescription" not in st.session_state:
    st.session_state["lexicalBundleDescription"] = "**Description:**"
if "original_script" not in st.session_state:
    st.session_state["original_script"] = ""
if "improved_script" not in st.session_state:
    st.session_state["improved_script"] = ""
if "list_of_lex" not in st.session_state:
    st.session_state["list_of_lex"] = {}
if "generate_script" not in st.session_state:
    st.session_state["generate_script"] = ""
if "old_sample_script" not in st.session_state:
    st.session_state["old_sample_script"] = ""
if "tips" not in st.session_state:
    st.session_state["tips"] = "**Tips:** Choose a type of lexical bundle to analyze!"
if "test" not in st.session_state:
    st.session_state["test"] = False

def gen_list_of_lex(generate_text_extract_table):
    list_of_lex = dict()
    for i in generate_text_extract_table:
        i = i.split('|')
        lex = i[3].strip()
        Type = i[4].strip()
        if(Type[0]!='x'):
            if(list_of_lex.get(Type[3:]) is not None):
                list_of_lex[Type[3:]].append(lex)
            else:
                list_of_lex[Type[3:]] = [lex]
    st.session_state["list_of_lex"] = list_of_lex

def update_status(text, icon):
    st.session_state["submission_status_text"] = text
    st.session_state["submission_status_icon"] = icon
    if(icon=="error"): st.rerun()

def check_script(script):
    # sentence_count = 0
    # for i in script:
    #     if i == ".":
    #         sentence_count = sentence_count + 1
    # if sentence_count > 20:
        # update_status(":red[Limited to a maximum of 20 sentences!]", "error")
        # st.rerun()
    # else:
    print("A script is submitted successfully!")
    print(st.session_state["original_script"])

    with open(f"./default.txt", 'w', encoding = "utf-8") as f:
        f.write(script)

    generate_script, generate_text_extract_table = main(default_path)
    # generate_script = "Now the technology has widely developed, TV, movies, computer online games and so on; an example of technology that has widely developed includes TV, movies, computer online games and so on. Although they made life better, it could be that it might be a problem, too. Elementary school students' nearsightedness is one of the problems. After school, the students have only less homework and they would do it quickly. Then some of the students may go outside to play with friends or play some sports like basketball or jogging. But most students just like to sit at home, watch TV, play computer games or sleep. Everyone hates it, but it just comes quietly. That's nothing wrong, but if they use them too much, it is important to note, it will be bad for their eyes, and if they continue this for a long time, they will have a serious problem: nearsighted. Go outside to see the beautiful sceneries, control the time that you watch TV or computer, and there will be the way to solve the problem."
    # generate_text_extract_table = [
    #     "| 1               | Now the technology has widely developed, TV, movies, computer online games [[and so on]]; [[an example of]] technology that has widely developed includes TV, movies, computer online games and so on.                               | and so on                | I. Quantity Specification         |",
    #     "| 1               | Now the technology has widely developed, TV, movies, computer online games and so on; an example of technology that has widely developed includes TV, movies, computer online games [[and so on]].                                    | an example of            | H. Identifier Phrase                  |"
    # ]
    st.session_state["improved_script"] = generate_script
    st.session_state["generate_script"] = generate_script
    st. session_state["tips"] = "**Tips:** Choose a type of lexical bundle to analyze!"
    st.session_state["lexicalBundleType"] = "**Type:**"
    st.session_state["lexicalBundleDescription"] = "**Description:**"

    gen_list_of_lex(generate_text_extract_table)
    update_status(":green[Ready to improve!]", "complete")
    st.rerun()

def show_button_description(type, description):
    if st.session_state["list_of_lex"].get(type) is None:
        st. session_state["tips"] = ":red[**Note:** Type not found!]"
    else:
        st. session_state["tips"] = ":green[**Note:** Type found!]"
    st.session_state["lexicalBundleType"] = "**Type:**" + " " + ":blue-background[" + type + "]"
    st.session_state["lexicalBundleDescription"] = "**Description:**" + " " + ":blue[" + description + "]"
    st.session_state["improved_script"] = st.session_state["generate_script"]
    if(st.session_state["list_of_lex"].get(type) is None):
        return
    for i in st.session_state["list_of_lex"][type]:
        st.session_state["improved_script"] = re.sub(i, ":blue-background["+ i +"]", st.session_state["improved_script"])

def use_sample_script(new_sample_script):
    # sample script may be written in a file
    if new_sample_script == "Sample: Student's Script 1":
        with open("./test_data/Default_original_input/student_01.txt", "r", encoding="utf-8") as f1:
            st.session_state["original_script"] = ''.join(f1.readlines())
    elif new_sample_script == "Sample: Student's Script 2":
        with open("./test_data/Default_original_input/student_02.txt", "r", encoding="utf-8") as f1:
            st.session_state["original_script"] = ''.join(f1.readlines())
    elif new_sample_script == "Sample: Lecturer's Script 1":
        with open("./test_data/Default_original_input/lecturer_01.txt", "r", encoding="utf-8") as f1:
            st.session_state["original_script"] = ''.join(f1.readlines())
    elif new_sample_script == "Sample: Lecturer's Script 2":
        with open("./test_data/Default_original_input/lecturer_02.txt", "r", encoding="utf-8") as f1:
            st.session_state["original_script"] = ''.join(f1.readlines())
    elif new_sample_script == "Input My Own Script":
        # with open("./test_data/Default_original_input/lecturer_02.txt", "r", encoding="utf-8") as f1:
        st.session_state["original_script"] = ""
    

st.set_page_config(layout="wide", page_title= "EMIighty", page_icon = ":scroll:")

st.title("*EMIighty*")
st.markdown("*The best EMI speech script assistant you can find.*")
st.divider()

upperLayout = st.container()
upperLayout.subheader("Original Script")
new_sample_script = upperLayout.selectbox(":gray[**Please select your input mode here :memo: :**]",
                                    ("Sample: Student's Script 1", "Sample: Student's Script 2", "Sample: Lecturer's Script 1", "Sample: Lecturer's Script 2", "Input My Own Script"),
                                    index = None,
                                    placeholder = "Here are some sample scripts for you to try if you want to ~",
                                    args = ())
# if new_sample_script != st.session_state["old_sample_script"]:
use_sample_script(new_sample_script)
userInput = upperLayout.form("user input", border = True)
original_script = userInput.text_area(":gray[**For 'Input My Own Script' mode, please input your script here** (limited to a maximum of 20 sentences) **:**]",
                                      value = st.session_state["original_script"],
                                      height = 300,
                                      label_visibility = "visible")
submission_status = userInput.status(st.session_state["submission_status_text"], state = st.session_state["submission_status_icon"])
if userInput.form_submit_button("**Submit**:airplane:", on_click = update_status, args = (":blue[Improving...]", "running")):
    check_script(original_script)

st.divider()

lowerLayout = st.container()
lowerLayout.subheader("Improved Script")
lowerCols = lowerLayout.container(border = True)
lowerCol1, lowerCol2 = lowerCols.columns([4, 1], vertical_alignment = "top")
lowerCol1.caption(":gray[**System Output:**]")
improvedScript = lowerCol1.container(height = 300, border = True)
improvedScript.markdown(st.session_state["improved_script"])
lexicalBundleList = lowerCol2.popover("**Types of Lexical Bundle :pencil2:**", use_container_width = True)
tips = lowerCol2.caption(st.session_state["tips"])
lowerCol2.markdown(st.session_state["lexicalBundleType"])
lowerCol2.markdown(st.session_state["lexicalBundleDescription"])
buttA = lexicalBundleList.button("Uncertain Statement", type = "secondary" if st.session_state["list_of_lex"].get("Uncertain Statement") is None else "primary", use_container_width = True, on_click = show_button_description, args = ("Uncertain Statement", "An 'Uncertain Statement' contains phrases expressing doubt or lack of certainty, indicating tentative or speculative assertions rather than definitive statements."))
buttB = lexicalBundleList.button("Obligation Statement", type = "secondary" if st.session_state["list_of_lex"].get("Obligation Statement") is None else "primary", use_container_width = True, on_click = show_button_description, args = ("Obligation Statement", "An 'Obligation Statement' contains phrases expressing a requirement or necessity, often directed at the second person pronoun, indicating actions deemed necessary or strongly recommended."))
buttC = lexicalBundleList.button("Intention and Prediction Statement", type = "secondary" if st.session_state["list_of_lex"].get("Intention and Prediction Statement") is None else "primary", use_container_width = True, on_click = show_button_description, args = ("Intention and Prediction Statement", "An 'Intention and Prediction Statement' contains phrases expressing the speaker's intention to perform future actions or indicating what is planned or expected to happen."))
buttD = lexicalBundleList.button("Ability Statement", type = "secondary" if st.session_state["list_of_lex"].get("Ability Statement") is None else "primary", use_container_width = True, on_click = show_button_description, args = ("Ability Statement", "An 'Ability Statement' describes skills or tasks that can be accomplished, often outlining what students should achieve."))
buttE = lexicalBundleList.button("Reference Statement", type = "secondary" if st.session_state["list_of_lex"].get("Reference Statement") is None else "primary", use_container_width = True, on_click = show_button_description, args = ("Reference Statement", "A 'Reference Statement' contains phrases referring to evidence, likelihood, or additional considerations, grounding assertions in observed or known information."))
buttF = lexicalBundleList.button("Topic Introduction", type = "secondary" if st.session_state["list_of_lex"].get("Topic Introduction") is None else "primary", use_container_width = True, on_click = show_button_description, args = ("Topic Introduction", "A 'Topic Introduction' statement signals the start of a new subject or area of discussion, using phrases that clearly indicate the instructor's intention to introduce and focus on a new topic."))
buttG = lexicalBundleList.button("Topic Elaboration", type = "secondary" if st.session_state["list_of_lex"].get("Topic Elaboration") is None else "primary", use_container_width = True, on_click = show_button_description, args = ("Topic Elaboration", "A 'Topic Elaboration' statement provides additional information or clarifies the current topic, helping to expand or deepen the discussion."))
buttH = lexicalBundleList.button("Identifier Phrase", type = "secondary" if st.session_state["list_of_lex"].get("Identifier Phrase") is None else "primary", use_container_width = True, on_click = show_button_description, args = ("Identifier Phrase", "An 'Identifier Phrase' emphasizes the importance of the following noun phrase, highlighting its significance or categorizing it."))
buttI = lexicalBundleList.button("Quantity Specification", type = "secondary" if st.session_state["list_of_lex"].get("Quantity Specification") is None else "primary", use_container_width = True, on_click = show_button_description, args = ("Quantity Specification", "A 'Quantity Specification' statement specifies the amount or extent of something, often quantifying aspects of the topic under discussion."))
buttJ = lexicalBundleList.button("Framing Attributes", type = "secondary" if st.session_state["list_of_lex"].get("Framing Attributes") is None else "primary", use_container_width = True, on_click = show_button_description, args = ("Framing Attributes", "A 'Framing Attributes' statement provides context or conditions that shape the understanding of the main subject."))
buttK = lexicalBundleList.button("Place/Time/Text Reference", type = "secondary" if st.session_state["list_of_lex"].get("Place/Time/Text Reference") is None else "primary", use_container_width = True, on_click = show_button_description, args = ("Place/Time/Text ReferencePlace/Time/Text Reference", "A 'Place/Time/Text Reference' statement indicates specific places, times, or locations within a text, providing clear references for context."))
buttL = lexicalBundleList.button("Opening and Disclosure", type = "secondary" if st.session_state["list_of_lex"].get("Opening and Disclosure") is None else "primary", use_container_width = True, on_click = show_button_description, args = ("Opening and Disclosure", "An 'Opening and Disclosure' statement signals the start or end of a discussion, presentation, or section, helping to structure the discourse by marking points of initiation or closure."))
buttM = lexicalBundleList.button("Citing Conversation", type = "secondary" if st.session_state["list_of_lex"].get("Citing Conversation") is None else "primary", use_container_width = True, on_click = show_button_description, args = ("Citing Conversation", "A 'Citing Conversation' statement recaps previous dialogues or comments, helping to reiterate and restructure established information within a conversation."))