"""Module for AI event creation processing functionalities"""

from io import BytesIO
import requests
from PIL import Image
from transformers import pipeline


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
        self.translation_pipe = pipeline("translation", model="facebook/mbart-large-50-many-to-many-mmt")
        self.languages = ['PL', 'EN', 'UA', 'RU']
        self.ai_languages_codes = {'PL': 'pl_PL', 'EN': 'en_XX', 'UA': 'uk_UA', 'RU': 'ru_RU'}
        self.fields_to_translate = ['name', 'description', 'shiftDirections']

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
                    data_dict = self.translate_array('shiftDirections', data_dict)
                else:
                    data_dict = self.translate_field(key, data_dict)

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

    def translate_array(self, array_name, dictionary):
        """
        Translates received array to desired languages

        Args:
            array_name (str): Sets which array we would like to translate, by its name
            dictionary (dict): Dictionary that will have a field translated

        Returns:
            dict: The same dictionary but with set array field deleted and generated fields with translated data
        """
        data = dictionary[array_name]
        shift_translations = []

        for direction in data:
            single_shift_translation = {}
            for lang in self.languages:
                field_key = f'addressDescription{lang}'
                if dictionary['language'] == lang:
                    single_shift_translation[field_key] = direction
                else:
                    if direction != "":
                        translation_result = self.translation_pipe(direction,
                                                                   src_lang=self.ai_languages_codes[
                                                                       dictionary['language']],
                                                                   tgt_lang=self.ai_languages_codes[lang])
                        single_shift_translation[field_key] = translation_result[0]['translation_text']
                    else:
                        single_shift_translation[field_key] = ""

            shift_translations.append(single_shift_translation)

        dictionary['shiftTranslations'] = shift_translations

        if array_name in dictionary:
            del dictionary[array_name]

        return dictionary

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