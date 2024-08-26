from flask import Flask, request, jsonify
from utils import search_articles, concatenate_content, generate_answer

app = Flask(__name__)

@app.route('/query', methods=['GET', 'POST'])
def query():
    # Get the user's query from the request
    data = request.get_json()
    query = data.get('query', '')

    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    # Step 1: Search and scrape articles based on the query
    articles = search_articles(query)
    
    # Step 2: Concatenate content from the scraped articles
    concatenated_content = concatenate_content(articles)
    
    # Step 3: Generate an answer using the LLM
    answer = generate_answer(concatenated_content, query)
    
    # Return the generated answer as JSON
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(host='localhost', port=5001, debug=True)

