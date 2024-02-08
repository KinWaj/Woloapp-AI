"""Main app for whole api"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from event_creation_app import EventCreationHandler
from category_suggester_app import SuggestionHandler

app = Flask(__name__)
CORS(app)

event_creation_handler = EventCreationHandler()
suggestion_handler = SuggestionHandler()


@app.route('/event-create', methods=['POST'])
def event_json_receiver():
    """Generate json with translation and alt generation"""
    try:
        received_json = request.json
        event_data_dict = event_creation_handler.translate_json(received_json)
        return jsonify(event_data_dict)
    except ValueError as value_error:
        return jsonify({'error': f'Invalid JSON data: {str(value_error)}'})


@app.route('/suggest', methods=['POST'])
def suggest_category_json_receiver():
    """Suggest category based on description"""
    try:
        received_json = request.json
        suggested_categories_dict = suggestion_handler.suggest_category(received_json)
        return jsonify(suggested_categories_dict)
    except ValueError as value_error:
        return jsonify({'error': f'Invalid JSON data: {str(value_error)}'})


if __name__ == '__main__':
    app.run(debug=True)
