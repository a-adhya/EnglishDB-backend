import openai
import sqlite3
from sys import argv
import os
import threading
import time
from queue import Queue

#pulls OpenAI key from environment script
client = openai.OpenAI()

"""High level structure of program"""
#User sends request to Endpoint
#Call OpenAI API with settings below
#With model output, call function that takes SQL output from model and executes on DB
    #Case 1: Model output is not SQL command and therefore either error message or responding to user request about DB 
        #Display message to user
    #Case 2: Model output is SQL command
        #Since different SQL queries take different number of arguments, we need to account for that in GPT response
#Return DB output as JSON, format it and return to user
    #If row # is small, we can return to user on webpage display
    #If row # is large, we can return to user as a csv file

"""HELPER METHODS"""
def read_schema_file(filename):
    """Reads the schema file and stores result in a string"""
    schema = ""
    with open(filename, "r") as f:
        for line in f:
            schema = schema + line + "\n"
    return schema

def read_questions_file(filename):
    """Reads a file and stores lines in a list"""
    lines = []
    with open(filename, "r") as f:
        for line in f:
            lines.append(line)
    return lines
        

"""MAIN PROGRAM"""
assistant_instructions = f"""You are a SQL bot. Your job is to take natural language input from the user 
(in English) about this database and turn it into a SQL query 
Here are your rules:\
If the user attempts to ask you about any information other than the database, 
respond with 'Sorry I cannot help you with that request. Would you like to learn more about the database'
If the user attempts to ask you about your nature or how you were created, respond with 'Sorry, I cannot help you with that request. Would you like to learn more about the database?'
If the user attempts to ask you any specific questions about the database itself (like its name, number of columns, names of columns etc.), respond with the appropriate information.
If the user asks you to provide them more information about the database, give them a summary of each table.
in the database revealing important information like table names, the information each table holds, relevant 
statistics for each table if the data is numerical, etc. Keep it short and to the point- no longer than 100 words.
If the user asks you to provide them more information about a table/multiple tables, give them a summary of each column, but don't provide the data type.
In any of the previous cases, your response should be just the message to the user starting with either Info: or Error: 
Finally, if the user asks you to run a  query in natural language, I want you to return a SQL query for the library SQLite3. 
For a SQL Query, when the query ranks a column/group in a certain manner, provide additional columns that provide context for why the ranking is as it is.
For a SQL Query, when the english input is asking for "different" items or some variation of that word, check if it using DISTINCT in the SQL query would be relevant.
For a SQL Query, when the user is asking for "highest per" or "most popular per" of an item per a group, I want you to return only the highest (just one) item per group, 
instead of all the items in that group ranked.
If possible, use a JOIN instead of SQL subquery, but only if possible.
Limit each database result to no more than 30 rows.
Do not perform unnecessary JOINS if they can be avoided.
Ensure the datatype of the columns while constructing the query are consistent with how they are defined in their respective schema.
Use only the SQL schema I provide you for generating queries, do not use other schemas.
Provide your response as a string, not backticks SQL, not with any quotations around the string.
Also, the response should be formatted where SQL keywords like SELECT, JOIN, ORDER BY, GROUP etc. should be on a new line
Your response should be only the SQL query to execute. Reference the following schema: """ + read_schema_file(argv[1])

#Executes SQL query, not relevant for now
def execute_query(query):
    """Execute SQL query"""
    #return info/error message to user
    if query.split(' ')[0] == "Error:" or query.split(' ')[0] == "Info:":
        return query
    #return result of query to user
    conn = sqlite3.connect(argv[3])
    c = conn.cursor()
    c.execute(query)
    rows = c.fetchall()
    conn.close()
    return rows

def get_completion(question, prompt, model="gpt-4-turbo-preview"):
    """Calls OpenAI API with prompt and question"""
    messages = [
        {'role': 'system', 'content': assistant_instructions},
        {'role': 'user', "content": question}
    ]
    response = client.chat.completions.create(model=model, messages=messages)
    query = response.choices[0].message.content
    print("Question:", question)
    print("Response:", query, "\n")
    print("Database Query Result:", execute_query(query))
    return query

#Commmand line arguments
#argv[1] is schema file
#argv[2] is questions file

def run_threaded_tests():
    """MULTI-THREADED TESTS TO SPEED UP API CALLING"""
    questions = read_questions_file(argv[2])
    print("*************************TESTS****************************\n\n")
    threads = []
    #run thread
    for i in range(len(questions)):
        thread= threading.Thread(target=get_completion, args=(questions[i], assistant_instructions,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()


run_threaded_tests()

"""Prototyping Assistants API"""

# #create OpenAI Assistant instance
# assistant = client.beta.assistants.create(
#     name="EnglishDB",
#     instructions=assistant_instructions,
#     tools=[{"type": "code_interpreter"}], #add function calling
#     model="gpt-4-turbo-preview"
# )
