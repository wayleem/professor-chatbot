from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot import predict_class, get_response, intents

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

@app.route('/api', methods=['OPTIONS'])
def options():
    return jsonify({"message": "This is the chatbot API"})

@app.route('/api', methods=['POST'])
def get_bot_response():
    message = request.json['message']
    ints = predict_class(message)
    res = get_response(ints, intents)
    tag = ints[0]['intent'] if ints else "unknown"
    
    points_change = 0

    if tag == "PositiveExcuse":
        points_change = 10
    elif tag == "NegativeExcuse":
        points_change = -5

    return jsonify({"response": res, "tag": tag, "points_change": points_change})

if __name__ == "__main__":
    app.run(debug=True)
