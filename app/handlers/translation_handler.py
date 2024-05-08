"""Module for handling AI translations processing functionalities"""

from .ai_utils.translation_util import TranslationTool


class TranslationHandler:
    """
    Handles translation processing of different formats: array or fields


    Methods:
        process_field_translation(json_data): Coordinates translation for a list of fields
        process_array_translation(json_data): Coordinates translation for a list of fields with array data
        language_delete(dict): Returns the same dictionary wiith no language field
    """

    def __init__(self, fields_to_translate, arrays_to_translate=None):
        """Init class - define field(s) to translate and initiate Translation Tool Util"""
        self.fields_to_translate = fields_to_translate
        self.arrays_to_translate = arrays_to_translate
        self.translation_tool = TranslationTool()
        print(self.arrays_to_translate)

    def process_field_translation(self, json_data):
        """
        Coordinates translation for a list of fields using TranslationTool Util

        Args:
            json_data (json): Json data with any fields - required: 'language'
                                and fields mentioned in self.fields_to_translate

        Returns:
            dict: Dictionary with translated fields
        """
        try:
            data_dict = dict(json_data)

            for key in self.fields_to_translate:
                data_dict = self.translation_tool.translate_field(field=key, dictionary=data_dict)

            return data_dict

        except KeyError as key_error:
            return {'error': f'Missing key: {str(key_error)}'}
        except ValueError as value_error:
            return {'error': f'Invalid JSON data: {str(value_error)}'}

    def process_array_translation(self, json_data):
        """
        Coordinates translation for a fields with array values using TranslationTool Util

        Args:
            json_data (json): Json data with any fields - required: 'language'
                                and field mentioned in self.fields_to_translate

        Returns:
            dict: Dictionary with translated fields
        """
        try:
            data_dict = dict(json_data)
            print(data_dict['shiftDirections'])

            for key in self.arrays_to_translate:
                print("key:", key)
                data_dict = self.translation_tool.translate_array(array_name=key, dictionary=data_dict)

            return data_dict

        except KeyError as key_error:
            return {'error': f'Missing key: {str(key_error)}'}
        except ValueError as value_error:
            return {'error': f'Invalid JSON data: {str(value_error)}'}

    def language_delete(self, dictionary):
        """
        Deletes language field from dictionary, if exists.

        Args:
            dictionary (dict): Dictionary that should have a language field

        Returns:
            dict: Dictionary with no language field
        """
        if 'language' in dictionary:
            del dictionary['language']

        return dictionary
