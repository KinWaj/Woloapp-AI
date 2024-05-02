"""Module for AI report translations processing functionalities"""

from .ai_utils.translation_util import TranslationTool


class ReportTranslationHandler:
    """
    Handles processing of report translation


    Methods:
        process_report_translation(json_data): Coordinates whole event creation processing, using TranslationTool Util
    """

    def __init__(self):
        """Init class - define field(s) to translate and initiate Translation Tool Util"""
        self.fields_to_translate = ['report']
        self.translation_tool = TranslationTool()

    def process_report_translation(self, json_data):
        """Coordinates report translation

        Args:
            json_data (json): Json data with any fields - required: 'language', 'report'

        Returns:
            dict: Dictionary with translated fields and no language:
                - report -> reportPL, reportEN, reportRU, reportUA"""
        try:
            data_dict = dict(json_data)

            # fields translations
            for key in self.fields_to_translate:
                data_dict = self.translation_tool.translate_field(field=key, dictionary=data_dict)

            # unused field deletion
            if 'language' in data_dict:
                del data_dict['language']

            return data_dict

        except KeyError as key_error:
            return {'error': f'Missing key: {str(key_error)}'}
        except ValueError as value_error:
            return {'error': f'Invalid JSON data: {str(value_error)}'}
