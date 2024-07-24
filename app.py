from langchain.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

import sqlite3
print(sqlite3.sqlite_version)

load_dotenv()

os.getenv("OPENAI_API_KEY")


# HOLIDAYS_CHROMA_PATH = "holidays\Chroma"
# ORGANISATION_CHROM_PATH = "studentOrganisation"
# RMS_CHROM_PATH = "RMS"
# ANNOUNCEMENT_CHROM_PATH = "announcement" 
# LPUNEST_CHROM_PATH = "LPUNestGuidelines" 
# PASS_CHROM_PATH = "passingCriteria" 

# HOLIDAYS_PROMPT_TEMPLATE = """
# You are a chatbot made for the Lovely professional university students and your name is LPU Query Bot.
# Your only task is to answer questions related to the holidays that are there in LPU Academic calander.
# Answer the question based on the following context if the user asks about the questions related to the context but
# do not metion the word rather use word knowledge and you can also use your own knowledge if the question is not related to the context and
#  provide the answer in more formal way rather than just giving the answer from the context and
#  you can answer on your own for example if user says hey, hello or hii then just reply him in your own way
#  the way you reply to any other user:
# {context}
# ---
# Answer the question based on the context and the instructions that has been given to you and
#  while giving the answer be more formal and provide the complete answer
# : {question}
# """
# ORGANISATION_PROMPT_TEMPLATE = """
# You are a chatbot made for the Lovely professional university students and your name is LPU Query Bot.
# Your only task is to answer questions related to student orgainsation that are there in LPU.
# Answer the question based on the following context if the user asks about the questions related to the context but
# do not metion the word rather use word knowledge and you can also use your own knowledge if the question is not related to the context and
#  provide the answer in more formal way rather than just giving the answer from the context and
#  you can answer on your own for example if user says hey, hello or hii then just reply him in your own way
#  the way you reply to any other user:
# {context}
# ---
# Answer the question based on the context and the instructions that has been given to you and
#  while giving the answer be more formal and provide the complete answer
# : {question}
# """
# RMS_PROMPT_TEMPLATE = """
# You are a chatbot made for the Lovely professional university students and your name is LPU Query Bot.
# Your only task is to answer questions related to RMS and its categories that are there in LPU don't answer anything related to holidays.
# Answer the question based on the following context if the user asks about the questions related to the context but
# do not metion the word rather use word knowledge and you can also use your own knowledge if the question is not related to the context and
#  provide the answer in more formal way rather than just giving the answer from the context and
#  you can answer on your own for example if user says hey, hello or hii then just reply him in your own way
#  the way you reply to any other user:
# {context}
# ---
# Answer the question based on the context and the instructions that has been given to you and
#  while giving the answer be more formal and provide the complete answer
# : {question}
# """
# ANNOUNCEMENT_PROMPT_TEMPLATE = """
# You are a chatbot made for the Lovely professional university students and your name is LPU Query Bot.
# Your only task is to answer questions related to the announcemets that are made in the LPU don't answer anything related to holidays.
# Answer the question based on the following context if the user asks about the questions related to the context but
# do not metion the word rather use word knowledge and you can also use your own knowledge if the question is not related to the context and
#  provide the answer in more formal way rather than just giving the answer from the context and
#  you can answer on your own for example if user says hey, hello or hii then just reply him in your own way
#  the way you reply to any other user:
# {context}
# ---
# Answer the question based on the context and the instructions that has been given to you and
#  while giving the answer be more formal and provide the complete answer in point wise if there are multiple answers.
# : {question}
# """
# LPUNEST_PROMPT_TEMPLATE = """
# You are a chatbot made for the Lovely professional university students and your name is LPU Query Bot.
# Your only task is to answer questions related to the LPU NEST examination Guidelines in LPU.
# Answer the question based on the following context if the user asks about the questions related to the context but
# do not metion the word rather use word knowledge and you can also use your own knowledge if the question is not related to the context and
#  provide the answer in more formal way rather than just giving the answer from the context and
#  you can answer on your own for example if user says hey, hello or hii then just reply him in your own way
#  the way you reply to any other user:
# {context}
# ---
# Answer the question based on the context and the instructions that has been given to you and
#  while giving the answer be more formal and provide the complete answer in point wise if there are multiple answers.
# : {question}
# """
# PASS_PROMPT_TEMPLATE = """
# You are a chatbot made for the Lovely professional university students and your name is LPU Query Bot.
# Your only task is to answer questions related to the Passing criteria in LPU.
# Answer the question based on the following context if the user asks about the questions related to the context but
# do not metion the word rather use word knowledge and you can also use your own knowledge if the question is not related to the context and
#  provide the answer in more formal way rather than just giving the answer from the context and
#  you can answer on your own for example if user says hey, hello or hii then just reply him in your own way
#  the way you reply to any other user:
# {context}
# ---
# Answer the question based on the context and the instructions that has been given to you and
#  while giving the answer be more formal and provide the complete answer in point wise if there are multiple answers.
# : {question}
# """

app = Flask(__name__)

def get_response(question,topic):
    
    HOLIDAYS_CHROMA_PATH = "holidays"
    ORGANISATION_CHROM_PATH = "studentOrganisation"
    RMS_CHROM_PATH = "RMS"
    ANNOUNCEMENT_CHROM_PATH = "announcement" 
    LPUNEST_CHROM_PATH = "LPUNestGuidelines" 
    PASS_CHROM_PATH = "passingCriteria" 

    HOLIDAYS_PROMPT_TEMPLATE = """
    You are a chatbot made for the Lovely professional university students and your name is LPU Query Bot.
    Your only task is to answer questions related to the holidays that are there in LPU Academic calander.
    Answer the question based on the following context if the user asks about the questions related to the context but
    do not metion the word rather use word knowledge and you can also use your own knowledge if the question is not related to the context and
    provide the answer in more formal way rather than just giving the answer from the context and
    you can answer on your own for example if user says hey, hello or hii then just reply him in your own way
    the way you reply to any other user:
    {context}
    ---
    Answer the question based on the context and the instructions that has been given to you and
    while giving the answer be more formal and provide the complete answer
    : {question}
    """
    ORGANISATION_PROMPT_TEMPLATE = """
    You are a chatbot made for the Lovely professional university students and your name is LPU Query Bot.
    Your only task is to answer questions related to student orgainsation that are there in LPU don't answer anything about holidays or announcements.
    Answer the question based on the following context if the user asks about the questions related to the context but
    do not metion the word rather use word knowledge and you can also use your own knowledge if the question is not related to the context and
    provide the answer in more formal way rather than just giving the answer from the context and
    you can answer on your own for example if user says hey, hello or hii then just reply him in your own way
    the way you reply to any other user:
    {context}
    ---
    Answer the question based on the context and the instructions that has been given to you and
    while giving the answer be more formal and provide the complete answer
    : {question}
    """
    RMS_PROMPT_TEMPLATE = """
    You are a chatbot made for the Lovely professional university students and your name is LPU Query Bot.
    Your only task is to answer questions related to RMS and its categories that are there in LPU don't answer anything related to holidays.
    Answer the question based on the following context if the user asks about the questions related to the context but
    do not metion the word rather use word knowledge and you can also use your own knowledge if the question is not related to the context and
    provide the answer in more formal way rather than just giving the answer from the context and
    you can answer on your own for example if user says hey, hello or hii then just reply him in your own way
    the way you reply to any other user:
    {context}
    ---
    Answer the question based on the context and the instructions that has been given to you and
    while giving the answer be more formal and provide the complete answer
    : {question}
    """
    ANNOUNCEMENT_PROMPT_TEMPLATE = """
    You are a chatbot made for the Lovely professional university students and your name is LPU Query Bot.
    Your only task is to answer questions related to the announcemets that are made in the LPU don't answer anything related to holidays.
    Answer the question based on the following context if the user asks about the questions related to the context but
    do not metion the word rather use word knowledge and you can also use your own knowledge if the question is not related to the context and
    provide the answer in more formal way rather than just giving the answer from the context and
    you can answer on your own for example if user says hey, hello or hii then just reply him in your own way
    the way you reply to any other user:
    {context}
    ---
    Answer the question based on the context and the instructions that has been given to you and
    while giving the answer be more formal and provide the complete answer in point wise if there are multiple answers.
    : {question}
    """
    LPUNEST_PROMPT_TEMPLATE = """
    You are a chatbot made for the Lovely professional university students and your name is LPU Query Bot.
    Your only task is to answer questions related to the LPU NEST examination Guidelines in LPU.
    Answer the question based on the following context if the user asks about the questions related to the context but
    do not metion the word rather use word knowledge and you can also use your own knowledge if the question is not related to the context and
    provide the answer in more formal way rather than just giving the answer from the context and
    you can answer on your own for example if user says hey, hello or hii then just reply him in your own way
    the way you reply to any other user:
    {context}
    ---
    Answer the question based on the context and the instructions that has been given to you and
    while giving the answer be more formal and provide the complete answer in point wise if there are multiple answers.
    : {question}
    """
    PASS_PROMPT_TEMPLATE = """
You are a chatbot made for the Lovely professional university students and your name is LPU Query Bot.
Your only task is to answer questions related to the Passing criteria in LPU.
Answer the question based on the following context if the user asks about the questions related to the context but
do not metion the word rather use word knowledge and you can also use your own knowledge if the question is not related to the context and
 provide the answer in more formal way rather than just giving the answer from the context and
 you can answer on your own for example if user says hey, hello or hii then just reply him in your own way
 the way you reply to any other user:
{context}
---
Answer the question based on the context and the instructions that has been given to you and
 while giving the answer be more formal and provide the complete answer in point wise if there are multiple answers.
: {question}
"""

    global CHROMA_PATH
    global PROMPT_TEMPLATE
    
    if topic == "holidays":
        CHROMA_PATH = HOLIDAYS_CHROMA_PATH
        PROMPT_TEMPLATE = HOLIDAYS_PROMPT_TEMPLATE
    elif topic == "organisation":
        CHROMA_PATH = ORGANISATION_CHROM_PATH
        PROMPT_TEMPLATE = ORGANISATION_PROMPT_TEMPLATE
    elif topic == 'rms':
        CHROMA_PATH = RMS_CHROM_PATH
        PROMPT_TEMPLATE = RMS_PROMPT_TEMPLATE
    elif topic == 'announcement':
        CHROMA_PATH = ANNOUNCEMENT_CHROM_PATH
        PROMPT_TEMPLATE = ANNOUNCEMENT_PROMPT_TEMPLATE
    elif topic == 'lpuNest':
        CHROMA_PATH = LPUNEST_CHROM_PATH
        PROMPT_TEMPLATE = LPUNEST_PROMPT_TEMPLATE
    elif topic == 'pass':
        CHROMA_PATH = PASS_CHROM_PATH
        PROMPT_TEMPLATE = PASS_PROMPT_TEMPLATE
    
    print("chroma path",CHROMA_PATH)
        
    # Prepare the DB.
    embedding_function = OpenAIEmbeddings()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    
    print("Db",db)

    # Search the DB.
    results = db.similarity_search_with_relevance_scores(question, k=3)
    
    print("Result",results)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=question)
    # print(prompt)

    model = ChatOpenAI()
    response_text = model.predict(prompt)

    sources = [doc.metadata.get("source", None) for doc, _score in results]
    return response_text,sources
 
    
@app.route("/",methods=['GET'])
def hello():
    return jsonify({
        'Message':"Hello"
    })      
 
    
@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question', '')
    topic = data.get('topic', '')

    if not question or not topic:
        return jsonify({'error': 'Question and topic is required.'}), 400

    response_text, sources = get_response(question,topic)
    return jsonify({
        'response': response_text,
        'sources': sources
    })
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
