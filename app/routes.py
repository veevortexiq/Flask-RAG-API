from flask import Blueprint, request, jsonify
from app.functions.cov import process_query
from app.functions.clean_response import cleanresponse
main = Blueprint('main', __name__)

@main.route('/process', methods=['POST'])
def process_message():
    data = request.json
    if 'query' in data:
        user_message = data['query']
        # Call your functions here
        result = (process_query(user_message))
        result = cleanresponse(result)
        print("cleaned_response",result)
        return jsonify({"response": result})
    return jsonify({"error": "Invalid input"}), 400