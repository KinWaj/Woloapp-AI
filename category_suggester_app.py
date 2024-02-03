"""Module for AI category suggester funtionalities"""
from setfit import SetFitModel


class SuggestionHandler:
    """Handles suggesting category based on recieved json with description"""
    def __init__(self):
        """Init class - create catrgories with ids"""
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

        return self.reformat_dict(category_suggested)

    def reformat_dict(self, category):
        """Return correct format based on suggested category name"""
        category_with_id_dict = {
            "name": category,
            "id": self.category_with_ids[category]
        }

        return category_with_id_dict
