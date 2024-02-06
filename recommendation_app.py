"""Module for AI recommender funtionalities"""
import pandas as pd
import requests
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MultiLabelBinarizer


class RecommendationHandler:
    """Handles recommending events"""
    def __init__(self):
        """Init class"""
        self.user_events_api_url = 'http://127.0.0.1:8080/users/{}/events'
        self.upcoming_events_api_url = "http://127.0.0.1:8080/events/upcoming"
        self.model = NearestNeighbors(n_neighbors=5, algorithm='auto')
        self.mlb = MultiLabelBinarizer()

    def recommend(self, json_data):
        data_dict = json_data
        user_id = data_dict["user_id"]

        user_events = list(self.get_users_events(user_id))

        upcoming_events = list(self.get_upcoming_events())

        all_events = user_events + upcoming_events

        events_df = pd.DataFrame(all_events)

        categories_matrix = self.mlb.fit_transform(events_df['categories'])
        districts_matrix = self.mlb.fit_transform(events_df['district'])
        organizations_matrix = self.mlb.fit_transform(events_df['organisation'])

        combined_matrix = pd.concat([pd.DataFrame(categories_matrix),
                                     pd.DataFrame(districts_matrix),
                                     pd.DataFrame(organizations_matrix)], axis=1)

        self.model.fit(combined_matrix)

        indices = self.model.kneighbors([self.mlb.transform(user_events).sum(axis=0)], return_distance=False)

        return upcoming_events

    def get_users_events(self, user_id):
        url = self.user_events_api_url.format(user_id)
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'API 1 request failed with status code {response.status_code}')

    def get_upcoming_events(self):
        response = requests.get(self.upcoming_events_api_url)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'API 1 request failed with status code {response.status_code}')