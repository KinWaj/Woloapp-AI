"""Module for AI category suggester functionalities"""
import requests
from setfit import SetFitModel


class SuggestionHandler:
    """
    Handles suggesting category using AI model.
    Huggingface: ayakiri/wolo-app-categories-setfit-model

    Methods:
        suggest_category(json_data): Suggest category of the event based on description; return category name and id
        reformat_dict(category): Formats response based on suggested category name
    """
    def __init__(self):
        self.categories_api_url = "http://127.0.0.1:8080/categories"
        self.category_with_ids = ({item['name']: item['id'] for item in self.get_all_categories()})

    def suggest_category(self, json_data):
        """
        Suggest category of the event based on description; return category name and id

        Args:
            json_data (json): Json data with one field with description of the event

        Returns:
            dict: Dictionary with two keys for suggested category - name and id
        """
        data_dict = dict(json_data)
        description = data_dict["description"]
        # pylint: disable=not-callable
        model = SetFitModel.from_pretrained("ayakiri/wolo-app-categories-setfit-model")
        category_suggested = model(description)

        return self.reformat_dict(category_suggested)

    def reformat_dict(self, category):
        """
        Formats response based on suggested category name

        Args:
            category (str): Name of the category based on which we will format a response

        Returns:
            dict: Dictionary with two keys for suggested category - name and id
        """
        category_with_id_dict = {
            "name": category,
            "id": self.category_with_ids[category]
        }

        return category_with_id_dict

    def get_all_categories(self):
        """
        Calls API and return a list of all categories

        Returns:
            list: List of dictionaries with category each with two keys for name and id
        """
        response = requests.get(self.categories_api_url) # pylint: disable=missing-timeout

        if response.status_code == 200:
            return response.json()
