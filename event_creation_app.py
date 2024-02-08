"""Module for AI translations funtionalities"""
from io import BytesIO

import requests
from PIL import Image
from transformers import pipeline


def load_image_from_url(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img


class EventCreationHandler:
    """Handles translations from recieved json with title, description, address description and language"""

    def __init__(self):
        """Init class - create model, tokenizer, define languages and ai languages codes"""
        self.translation_pipe = pipeline("translation", model="facebook/mbart-large-50-many-to-many-mmt")
        self.visual_pipe = pipeline("image-to-text", model="microsoft/git-base-coco")
        self.languages = ['PL', 'ENG', 'UA', 'RU']
        self.ai_languages_codes = {'PL': 'pl_PL', 'ENG': 'en_XX', 'UA': 'uk_UA', 'RU': 'ru_RU'}

    def translate_json(self, json_data):
        """Translates recieved json data with AI and returns modified dictionary.
         Creates keys for every language separately"""
        try:
            data_dict = dict(json_data)

            for key in ['name', 'description', 'addressDescription']:
                data_dict = self.translate_field(key, data_dict)

            if 'language' in data_dict:
                del data_dict['language']

            if data_dict["imageUrl"] != "":
                data_dict["alt"] = self.generate_alt(data_dict["imageUrl"])

            return data_dict

        except KeyError as key_error:
            return {'error': f'Missing key: {str(key_error)}'}
        except ValueError as value_error:
            return {'error': f'Invalid JSON data: {str(value_error)}'}

    def translate_field(self, field, dictionary):
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
        img = load_image_from_url(url)

        result = self.visual_pipe(img)

        return result[0]["generated_text"]
