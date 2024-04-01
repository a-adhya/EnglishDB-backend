from flask import Flask, request, jsonify
from sys import argv, stderr
import openai
import sqlite3
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
client = openai.OpenAI()

# Dictionary mapping database names to SQLite database file paths
DATABASES = {
    'Media DB': 'src/dbs/media.sqlite3',
    'Car Sales DB': 'src/dbs/carsales.sqlite3',
    'Products DB': 'src/dbs/office.sqlite3',
}

SCHEMAS = {
    'Media DB': 'src/schemas/media_schema.sql',
    'Car Sales DB': 'src/schemas/carsales_schema.sql',
    'Products DB': 'src/schemas/office_schema.sql',
}

def read_schema_file(filename):
    """Reads the schema file and stores result in a string"""
    schema = ""
    with open(filename, "r") as f:
        for line in f:
            schema = schema + line + "\n"
    return schema

#Executes SQL query, not relevant for now
def execute_query(database, sql_query):
    """Execute SQL query"""
    try:
        conn = sqlite3.connect(DATABASES[database])
        conn.row_factory = sqlite3.Row  # This enables column header support
        cur = conn.cursor()
    except Exception as e:
        print("Error:", e, file=stderr)

    cur.execute(sql_query)
    rows = cur.fetchall()
    # Convert rows to dict to include column headers
    result = [dict(row) for row in rows]
    conn.close()
    return result

def get_completion(question, instructions, model="gpt-4-turbo-preview"):
    """Calls OpenAI API with prompt and question"""
    messages = [
        {'role': 'system', 'content': instructions},
        {'role': 'user', "content": question}
    ]
    response = client.chat.completions.create(model=model, messages=messages)
    query = response.choices[0].message.content
    print("Question:", question, file=stderr)
    print("Response:", query, file=stderr)
    return query

@app.route('/app/<database>', methods=['POST'])
@cross_origin()
def query_database(database):
    # Check if the database exists
    if database not in DATABASES:
        return jsonify({'error': 'Database not found'}), 404
    
    """MAIN ASSISTANT PROMPT"""
    assistant_instructions = f"""You are a SQL bot. Your job is to take natural language input from the user 
    (in English) about this database and turn it into a SQL query 
    Here are your rules:\
    If the user attempts to ask you any specific questions about the database itself (like its name, number of columns, names of columns etc.), respond with the appropriate information.
    If the user asks you to provide them more information about the database, give them a summary of each table 
    in the database revealing important information like table names, the information each table holds, relevant 
    statistics for each table if the data is numerical, etc. Keep it short and to the point- no longer than 100 words.
    If the user asks you to provide them more information about a table/multiple tables, give them a summary of each column, but don't provide the data type.
    In any of the previous cases, your response should be just the message to the user ALWAYS starting with Info:
    If the user attempts to ask you about any information other than the database, 
    respond with 'Error: Sorry I cannot help you with that request. Would you like to learn more about the database'
    If the user attempts to ask you about your nature or how you were created, 
    respond with 'Error: Sorry, I cannot help you with that request. Would you like to learn more about the database?'
    Finally, if the user asks you to run a query in natural language, I want you to return a SQL query for the library SQLite3. 
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
    Your response should be only the SQL query to execute. Reference the following schema: """ + read_schema_file(SCHEMAS[database])
    # Get the English query from the form data
    english_query = request.form.get('query')
    if not english_query:
        return jsonify({'error': 'No query provided'}), 400
    # Call the OpenAI API to convert the English query into an SQL statement
    # Execute the SQL statement against the database
    try:
        sql_query = get_completion(english_query, assistant_instructions)
        if sql_query.split(' ')[0] == 'Info:' or sql_query.split(' ')[0] == 'Error:':
            return jsonify({
            'sql_query': sql_query,
            'query_result': 'InfoError'
            })
        result = execute_query(database, sql_query)
    except Exception as e:
        return jsonify({'error': f'Failed to generate SQL query: {e}'}), 500

    # Return the SQL statement and the query results
    return jsonify({
        'sql_query': sql_query,
        'query_result': result
    })

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)
