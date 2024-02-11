"""Module for AI event creation processing functionalities"""

from io import BytesIO
import requests
from PIL import Image
from transformers import pipeline
from exceptions.inappropriate_event_exception import InappropriateEventException


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
    Hate speech detection - huggingface: IMSyPP/hate_speech_en


    Methods:
        process_event_creation(json_data): Coordinates whole event creation processing
        translate_field(field, dictionary): Translates received field to desired languages
        generate_alt(url): Generates an Alt text for an image
        hate_speech_detection(description): Classifies description into one of four classes and provides probability
    """

    def __init__(self):
        """Init class - create model, tokenizer, define languages and ai languages codes"""
        self.translation_pipe = pipeline("translation", model="facebook/mbart-large-50-many-to-many-mmt")
        self.languages = ['PL', 'EN', 'UA', 'RU']
        self.ai_languages_codes = {'PL': 'pl_PL', 'EN': 'en_XX', 'UA': 'uk_UA', 'RU': 'ru_RU'}
        self.fields_to_translate = ['name', 'description', 'addressDescription']

        self.visual_pipe = pipeline("image-to-text", model="microsoft/git-base-coco")

        self.hate_speech_pipeline = pipeline("text-classification", model="IMSyPP/hate_speech_en")
        self.inappropriate_labels = ["LABEL_1", "LABEL_2", "LABEL_3"]

    def process_event_creation(self, json_data):
        """
        Coordinates whole event creation processing

        Args:
            json_data (json): Json data with any fields - required: name, description, addressDescription

        Returns:
            dict: Dictionary with the same fields that were received and more:
                - name -> namePL, nameEN, nameRU, nameUA;
                - description -> descriptionPL, descriptionEN, descriptionRU, descriptionUA;
                - addressDescription -> addressDescriptionPL, addressDescriptionEND, addressDescriptionRU,
                                        addressDescriptionUA;
                - generates alt if imageURL provided
                - returns different json with error and error code if description ris inappropriate
        """
        try:
            data_dict = dict(json_data)

            # fields translations
            for key in self.fields_to_translate:
                data_dict = self.translate_field(key, data_dict)

            # hate speech detection
            is_inappropriate = self.hate_speech_pipeline(data_dict["descriptionEN"])

            if is_inappropriate[0]['label'] in self.inappropriate_labels:
                raise InappropriateEventException()

            # unused field deletion
            if 'language' in data_dict:
                del data_dict['language']

            # alt text generation
            if data_dict["imageUrl"] != "":
                data_dict["alt"] = self.generate_alt(data_dict["imageUrl"])

            return data_dict

        except KeyError as key_error:
            return {'error': f'Missing key: {str(key_error)}'}
        except ValueError as value_error:
            return {'error': f'Invalid JSON data: {str(value_error)}'}

    def translate_field(self, field, dictionary):
        """
        Translates received field to desired languages

        Args:
            field (str): Sets which field we would like to translate
            dictionary (dict): Dictionary that will have a field translated

        Returns:
            dict: The same dictionary but with set field deleted and generated fields with translated data
        """
        for lang in self.languages:
            lang_key = f'{field}{lang}'
            if dictionary['language'] == lang:
                dictionary[lang_key] = f'{dictionary[field]}'
            else:
                if dictionary[field] != "":
                    # AI translations using pipeline
                    translation_result = self.translation_pipe(dictionary[field],
                                                               src_lang=self.ai_languages_codes[dictionary['language']],
                                                               tgt_lang=self.ai_languages_codes[lang])
                    dictionary[lang_key] = translation_result[0]['translation_text']
                else:
                    dictionary[lang_key] = ""

        if field in dictionary:
            del dictionary[field]

        return dictionary

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

    def hate_speech_detection(self, description):
        """
        Classifies description into one of four classes:
        LABEL_0 - acceptable
        LABEL_0 - inappropriate
        LABEL_0 - offensive
        LABEL_0 - violent
        And provides probability

        Args:
            description (str): Description to analyze

        Returns:
            list: List with dictionary with label and probability
        """
        result = self.hate_speech_pipeline(description)

        return result
