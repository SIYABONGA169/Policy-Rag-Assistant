"""
Flask Web Application for RAG-Based Company Policy Assistant

This script implements FR-5: Application Endpoints & User Interface
- GET /: Serves the web chat interface
- POST /chat: Accepts questions and returns answers with citations
- GET /health: Health check endpoint
"""

from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify, render_template
from rag import answer_question

app = Flask(__name__)


@app.route('/')
def index():
    """Serve the web chat interface."""
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    """
    Accept a question and return the answer with citations and snippets.
    
    Expected JSON payload:
    {
        "question": "What is the company policy on annual leave?",
        "chat_history": []  # Optional: list of previous conversation messages
    }
    
    Returns JSON with answer, citations, and snippets.
    """
    try:
        data = request.get_json()
        
        # Validate request
        if not data:
            return jsonify({'error': 'Request body must be JSON'}), 400
        
        if 'question' not in data:
            return jsonify({'error': 'Missing "question" field'}), 400
        
        question = data['question']
        chat_history = data.get('chat_history', None)
        
        # Validate question is not empty
        if not question or not question.strip():
            return jsonify({
                'answer': 'I can only answer questions related to company policies and procedures.',
                'citations': [],
                'snippets': []
            }), 200
        
        # Call RAG pipeline with optional chat history
        result = answer_question(question, chat_history=chat_history)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'}), 200


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
