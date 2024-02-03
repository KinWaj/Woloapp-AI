"""Module for AI category suggester funtionalities"""
from setfit import SetFitModel


class SuggestionHandler:
    def __init__(self):
        self.category_with_ids = {"Kultura": 1,
                                  "Sport": 2,
                                  "Edukacja": 3,
                                  "Ekologia": 4,
                                  "Pomoc": 5}

    def suggest_category(self, json_data):
        """Uses woloapp own model to suggest category based on description, return category name and id"""
        data_dict = dict(json_data)
        description = data_dict["description"]
        # pylint: disable=not-callable
        model = SetFitModel.from_pretrained("ayakiri/wolo-app-categories-setfit-model")
        category_suggested = model(description)

        category_suggested_dict = {
            "name": category_suggested,
            "id": self.category_with_ids[category_suggested]
        }

        return category_suggested_dict
