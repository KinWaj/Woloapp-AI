"""Main app for whole api with endpoints"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from handlers.event_creation_handler import EventCreationHandler

app = Flask(__name__)
CORS(app)

event_creation_handler = EventCreationHandler()


@app.route('/event-create', methods=['POST'])
def event_creation_json_receiver():
    """
    Receiver for creating event. Responsible for translating fields, generating alt text for images and checks if 
    description is appropriate.
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


if __name__ == '__main__':
    app.run(debug=True)
