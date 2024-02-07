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
        """Recommends upcoming events based on user events. Needs to recieve json_data with user id"""
        data_dict = json_data
        user_id = data_dict["user_id"]

        user_events = list(self.get_users_events(user_id))
        upcoming_events = list(self.get_upcoming_events())

        user_matrix = self.prepare_matrix()
        user_matrix = self.insert_events(user_events, user_matrix)

        all_matrix = self.prepare_matrix()
        all_matrix = self.insert_events(user_events, all_matrix)
        all_matrix = self.insert_events(upcoming_events, all_matrix)

        # printing for debugging proces, to be deleted
        pd.set_option('display.max_columns', None)
        pd.set_option('display.expand_frame_repr', False)
        print("USER")
        print(user_matrix)
        print("ALL")
        print(all_matrix)

        #TODO - use binary matrixes to create model and predict - NOT WORKING

        self.mlb.fit(all_matrix)
        transformed_user_matrix = self.mlb.transform(user_matrix)
        print(transformed_user_matrix)
        self.model.fit(all_matrix)

        indices = self.model.kneighbors([self.mlb.transform(transformed_user_matrix).sum(axis=0)], return_distance=False)

        print(indices)

        return upcoming_events

    def get_users_events(self, user_id):
        """Calls API and return a list of events that user participated in"""
        # url = self.user_events_api_url.format(user_id)
        # response = requests.get(url)
        #
        # if response.status_code == 200:
        #     return response.json()
        # else:
        #     raise Exception(f'API 1 request failed with status code {response.status_code}')

        json_dummy = [
                  {
                    "id": 9,
                    "organisation": "PJATK",
                    "district": "Orunia",
                    "categories": ["Sport"]
                  },
                  {
                    "id": 10,
                    "organisation": "PJATK",
                    "district": "Centrum",
                    "categories": ["Sport"]
                  },
                  {
                    "id": 11,
                    "organisation": "Kwiatuszek",
                    "district": "Wrzeszcz",
                    "categories": ["Ekologia", "Pomoc"]
                  }
                ]

        return json_dummy


    def get_upcoming_events(self):
        """Calls API and return a list of upcoming events"""
        # response = requests.get(self.upcoming_events_api_url)
        #
        # if response.status_code == 200:
        #     return response.json()
        # else:
        #     raise Exception(f'API 1 request failed with status code {response.status_code}')

        json_dummy = [
                      {
                        "id": 1,
                        "organisation": "Kwiatuszek",
                        "district": "Wrzeszcz",
                        "categories": ["Sport"]
                      },
                      {
                        "id": 2,
                        "organisation": "Bananek",
                        "district": "Przymorze",
                        "categories": ["Edukacja"]
                      },
                      {
                        "id": 3,
                        "organisation": "PJATK",
                        "district": "Orunia",
                        "categories": ["Sport", "Pomoc"]
                      },
                      {
                        "id": 4,
                        "organisation": "PJATK",
                        "district": "Centrum",
                        "categories": ["Sport"]
                      },
                      {
                        "id": 5,
                        "organisation": "Bananek",
                        "district": "Wrzeszcz",
                        "categories": ["Kultura"]
                      },
                      {
                        "id": 6,
                        "organisation": "Kwiatuszek",
                        "district": "Wrzeszcz",
                        "categories": ["Ekologia", "Pomoc"]
                      },
                      {
                        "id": 7,
                        "organisation": "Pieski i kotki",
                        "district": "Orunia",
                        "categories": ["Ekologia", "Pomoc"]
                      },
                      {
                        "id": 8,
                        "organisation": "Bananek",
                        "district": "Przymorze",
                        "categories": ["Kultura"]
                      }
                    ]

        return json_dummy

    def prepare_matrix(self):
        """Prepare an empty matrix with all columns from API - categories, districts and organisations"""
        # TODO - Import from API
        categories = {
            "categories": ["Kultura", "Sport", "Edukacja", "Ekologia", "Pomoc", "Podstawowa"]
        }
        districts = {
            "districts": ["Wrzeszcz", "Centrum", "Przymorze", "Chelm", "Zaspa", "Oliwa", "Orunia"]
        }
        organisations = {
            "organisations": ["Wesoly Senior", "Przedszkole Tecza", "ChessMaster", "Fundacja Druga Szansa", "PJATK", "Kwiatuszek", "Bananek", "Pieski i kotki"]
        }

        all_columns = [categories["categories"], districts["districts"], organisations["organisations"]]
        all_columns = [item for sublist in all_columns for item in sublist]

        df = pd.DataFrame(all_columns).transpose()
        df.columns = df.iloc[0]
        df = df[1:]

        return df

    def insert_events(self, events_list, df):
        """Goes through list of events and inserts a rows to binary matrix"""
        for event in events_list:
            row_data = [0] * len(df.columns)

            for category in event.get('categories', []):
                row_data[df.columns.get_loc(category)] = 1

            row_data[df.columns.get_loc(event['district'])] = 1
            row_data[df.columns.get_loc(event['organisation'])] = 1

            df.loc[len(df)] = row_data

        return df

