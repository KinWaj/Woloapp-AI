"""Main app for whole api with endpoints"""
import warnings

from flask import Flask, request, jsonify
from flask_cors import CORS
from handlers.translation_handler import TranslationHandler

warnings.filterwarnings(
    "ignore",
    category=FutureWarning,
    message="`resume_download` is deprecated and will be removed in version 1.0.0"
)

app = Flask(__name__)
CORS(app)


@app.route('/event-create', methods=['POST'])
def event_creation_json_receiver():
    """
    Receiver for creating event. Responsible for translating fields of event including single fields and arrays.
    method: POST

    Returns:
        json: Json data with the same fields that were received and more:
                - name -> namePL, nameEN, nameRU, nameUA;
                - description -> descriptionPL, descriptionEN, descriptionRU, descriptionUA;
                - shiftDirections -> array of objects with addressDescriptionPL, addressDescriptionEND,
                                    addressDescriptionRU, addressDescriptionUA.

    Raises:
        ValueError: Not correct JSON data
    """
    try:
        received_json = request.json
        handler = TranslationHandler(fields_to_translate=['name', 'description'],
                                     arrays_to_translate=['shiftDirections'])
        event_data_dict = handler.process_field_translation(received_json)
        event_data_dict = handler.process_array_translation(event_data_dict)
        event_data_dict = handler.language_delete(event_data_dict)

        return jsonify(event_data_dict)
    except ValueError as value_error:
        return jsonify({'error': f'Invalid JSON data: {str(value_error)}'})


@app.route('/report/translate', methods=['POST'])
def report_json_receiver():
    """
    Receiver for translating a report.
    Responsible for translating report text from received json.
    method: POST

    Raises:
        ValueError: Not correct JSON data
    """
    try:
        received_json = request.json
        handler = TranslationHandler(fields_to_translate=['report'])
        report_dict = handler.process_field_translation(received_json)
        report_dict = handler.language_delete(report_dict)
        return jsonify(report_dict)
    except ValueError as value_error:
        return jsonify({'error': f'Invalid JSON data: {str(value_error)}'})


@app.route('/organisation/translate', methods=['POST'])
def organisation_json_receiver():
    """
    Receiver for translating an organisation.
    Responsible for translating organisation description text from received json.
    method: POST

    Raises:
        ValueError: Not correct JSON data
    """
    try:
        received_json = request.json
        handler = TranslationHandler(fields_to_translate=['description'])
        organisation_json = handler.process_field_translation(received_json)
        organisation_json = handler.language_delete(organisation_json)
        return jsonify(organisation_json)
    except ValueError as value_error:
        return jsonify({'error': f'Invalid JSON data: {str(value_error)}'})


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port='5000')
