from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot import get_bot_response

app = Flask(__name__)
CORS(app)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        bot_response = get_bot_response(user_message)
        return jsonify({'response': bot_response})
    except Exception as e:
        print(f"Error in API call: {str(e)}")
        return jsonify({'response': 'Error processing request'}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)