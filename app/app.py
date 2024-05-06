"""Main app for whole api with endpoints"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from handlers.event_creation_handler import EventCreationHandler
from handlers.report_translation_handler import ReportTranslationHandler
from handlers.organisation_creation_handler import OrganisationCreationHandler

app = Flask(__name__)
CORS(app)

event_creation_handler = EventCreationHandler()
report_translation_handler = ReportTranslationHandler()
organisation_creation_handler = OrganisationCreationHandler()


@app.route('/event-create', methods=['POST'])
def event_creation_json_receiver():
    """
    Receiver for creating event. Responsible for translating fields, generating alt text for images.
    endpoint: /event-create
    method: POST

    Returns:
        json: Json data with the same fields that were received and more:
                - name -> namePL, nameEN, nameRU, nameUA;
                - description -> descriptionPL, descriptionEN, descriptionRU, descriptionUA;
                - addressDescription -> addressDescriptionPL, addressDescriptionEND, addressDescriptionRU,
                                        addressDescriptionUA;
                - generates alt if imageURL provided
                - returns different json with error and error code if description ris inappropriate

    Raises:
        InappropriateEventException: Detected inappropriate event description
        ValueError: Not correct JSON data
    """
    try:
        received_json = request.json
        event_data_dict = event_creation_handler.process_event_creation(received_json)
        return jsonify(event_data_dict)
    except ValueError as value_error:
        return jsonify({'error': f'Invalid JSON data: {str(value_error)}'})


@app.route('/report/translate', methods=['POST'])
def report_json_receiver():
    """
    Receiver for translating a report. Responsible for translating report text from received json.
    """
    try:
        received_json = request.json
        report_dict = report_translation_handler.process_report_translation(received_json)
        return jsonify(report_dict)
    except ValueError as value_error:
        return jsonify({'error': f'Invalid JSON data: {str(value_error)}'})


@app.route('/organisation/translate', methods=['POST'])
def organisation_json_receiver():
    """
    Receiver for translating an organisation. Responsible for translating organisation description text from received json.
    """
    try:
        received_json = request.json
        organisation_json = organisation_creation_handler.process_organisation_creation(received_json)
        return jsonify(organisation_json)
    except ValueError as value_error:
        return jsonify({'error': f'Invalid JSON data: {str(value_error)}'})


if __name__ == '__main__':
    app.run(debug=True)
