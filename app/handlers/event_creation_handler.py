"""Module for AI event creation processing functionalities"""

from io import BytesIO
import requests
from PIL import Image
from transformers import pipeline
from .ai_utils.translation_util import TranslationTool


def load_image_from_url(url):
    """
    Loads an image from a URL

    Returns:
        Image: loaded image data in bytes
    """
    response = requests.get(url)  # pylint: disable=missing-timeout
    img = Image.open(BytesIO(response.content))
    return img


class EventCreationHandler:
    """
    Handles processing of event creation using different AI models.
    Translations - huggingface: facebook/mbart-large-50-many-to-many-mmt
    Alt text generator - huggingface: microsoft/git-base-coco


    Methods:
        process_event_creation(json_data): Coordinates whole event creation processing
        translate_field(field, dictionary): Translates received field to desired languages
        generate_alt(url): Generates an Alt text for an image
    """

    def __init__(self):
        """Init class - create model, tokenizer, define languages and ai languages codes"""
        self.fields_to_translate = ['name', 'description', 'shiftDirections']
        self.translation_tool = TranslationTool()

        self.visual_pipe = pipeline("image-to-text", model="microsoft/git-base-coco")

    def process_event_creation(self, json_data):
        """
        Coordinates whole event creation processing

        Args:
            json_data (json): Json data with any fields - required: name, description, shiftDirections

        Returns:
            dict: Dictionary with the same fields that were received and more:
                - name -> namePL, nameEN, nameRU, nameUA;
                - description -> descriptionPL, descriptionEN, descriptionRU, descriptionUA;
                - for every record in shiftDirections -> addressDescriptionPL,
                                                        addressDescriptionEND,
                                                        addressDescriptionRU,
                                                        addressDescriptionUA;
                - generates alt if imageURL provided
        """
        try:
            data_dict = dict(json_data)

            # fields translations
            for key in self.fields_to_translate:
                if key == 'shiftDirections':
                    data_dict = self.translation_tool.translate_array('shiftDirections', data_dict)
                else:
                    data_dict = self.translation_tool.translate_field(key, data_dict)

            # unused field deletion
            if 'language' in data_dict:
                del data_dict['language']

            # alt text generation
            if data_dict["imageUrl"] != "":
                data_dict["alt"] = self.generate_alt(data_dict["imageUrl"])

            if 'imageUrl' in data_dict:
                del data_dict['imageUrl']

            return data_dict

        except KeyError as key_error:
            return {'error': f'Missing key: {str(key_error)}'}
        except ValueError as value_error:
            return {'error': f'Invalid JSON data: {str(value_error)}'}

    def generate_alt(self, url):
        """
        Generates an Alt text for an image

        Args:
            url (str): Url of an image that needs to have alt text

        Returns:
            str: Generated alt text in plain string format
        """
        img = load_image_from_url(url)

        result = self.visual_pipe(img)

        return result[0]["generated_text"]
