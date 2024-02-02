"""Module for AI category suggester funtionalities"""

from flask import Flask, request, jsonify
from setfit import SetFitModel

app = Flask(__name__)


def suggest_category(json_data):
    data_dict = dict(json_data)
    description = data_dict["description"]

    model = SetFitModel.from_pretrained("ayakiri/wolo-app-categories-setfit-model")
    category_suggested = model(description)

    return category_suggested


@app.route('/suggest', methods=['POST'])
def suggest_category_json_receiver():
    """Receives json with description to suggest a category based on it"""
    try:
        received_json = request.json

        suggested_categories_dict = suggest_category(received_json)

        return jsonify(suggested_categories_dict)

    except ValueError as value_error:
        return jsonify({'error': f'Invalid JSON data: {str(value_error)}'})


if __name__ == '__main__':
    app.run(debug=True)
