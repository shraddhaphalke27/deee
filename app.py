from flask import Flask, render_template, request
from database_connector import execute_sql_query
from gensql import generate_new_trial
 
app = Flask(__name__)
 
@app.route('/', methods=['GET', 'POST'])
def index():
    sql_query = None
    results = None
    columns = None
 
    if request.method == 'POST':
        user_input = request.form['user_input']
        # Generate SQL query using gensql.py
        sql_query = generate_new_trial(user_input)
 
        if sql_query:
            # Execute the generated SQL query
            columns, raw_results = execute_sql_query(sql_query)
            # Remove duplicate results
            results = [list(row) for row in set(tuple(r) for r in raw_results)]
    return render_template('index.html', sql_query=sql_query, results=results, columns=columns)
 
if __name__ == '__main__':
    app.run(debug=True)

