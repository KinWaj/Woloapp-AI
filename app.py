from flask import Flask, request, jsonify
from translations_app import TranslationHandler
from category_suggester_app import SuggestionHandler

app = Flask(__name__)

translation_handler = TranslationHandler()
suggestion_handler = SuggestionHandler()


@app.route('/translate', methods=['POST'])
def translate_json_receiver():
    try:
        received_json = request.json
        translated_data_dict = translation_handler.translate_json(received_json)
        return jsonify(translated_data_dict)
    except ValueError as value_error:
        return jsonify({'error': f'Invalid JSON data: {str(value_error)}'})


@app.route('/suggest', methods=['POST'])
def suggest_category_json_receiver():
    try:
        received_json = request.json
        suggested_categories_dict = suggestion_handler.suggest_category(received_json)
        return jsonify(suggested_categories_dict)
    except ValueError as value_error:
        return jsonify({'error': f'Invalid JSON data: {str(value_error)}'})


if __name__ == '__main__':
    app.run(debug=True)
