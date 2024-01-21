"""Module for AI functionalities - recommendation system"""

from flask import Flask, request, jsonify

app = Flask(__name__)

ALL_EVENTS_URL = "/events"
EVENT_WITH_ID_URL = "/events/"


def get_all_events():
    """Calls API and returns a json with all events"""
    response = request.get(ALL_EVENTS_URL)

    if response.status_code == 200:
        all_events_data = dict(response.json())
        return all_events_data
    else:
        return None


def get_event_information(event_id):
    """Calls API and returns district and categories from event with specific id"""
    url = EVENT_WITH_ID_URL + event_id

    response = request.post(url)

    districts_and_categories = []

    if response.status_code == 200:
        event_info_data = dict(response.json())

        return event_info_data
    else:
        return None


def recommend_events(json_data):
    """I don't know"""
    participated_events_ids = dict(json_data)["events_id"]

    for event in participated_events_ids:
        # handle extracting districts and categories
        print(event)

    return participated_events_ids


@app.route('/recommend', methods=['POST'])
def recommend_json_receiver():
    """Receives json and give back recomendations (ids of events)"""
    try:
        received_json = request.json

        recommended_events = recommend_events(received_json)

        return jsonify(recommended_events)

    except ValueError as value_error:
        return jsonify({'error': f'Invalid JSON data: {str(value_error)}'})


if __name__ == '__main__':
    app.run(debug=True)
