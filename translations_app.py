"""Module for AI translations funtionalities"""
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast


class TranslationHandler:
    """Handles translations from recieved json with title, description, address description and language"""

    def __init__(self):
        """Init class - create model, tokenizer, define languages and ai languages codes"""
        self.model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
        self.tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
        self.languages = ['PL', 'ENG', 'UA', 'RU']
        self.ai_languages_codes = {'PL': 'pl_PL', 'ENG': 'en_XX', 'UA': 'pl_PL', 'RU': 'pl_PL'}

    def translate_json(self, json_data):
        """Translates recieved json data with AI and returns modified dictionary.
         Creates keys for every language separately"""
        try:
            data_dict = dict(json_data)

            model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
            tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")

            # TODO - add coding for uk and ru
            languages = ['PL', 'ENG', 'UA', 'RU']
            ai_languages_codes = {
                'PL': 'pl_PL',
                'ENG': 'en_XX',
                'UA': 'pl_PL',
                'RU': 'pl_PL'
            }

            for key in ['title', 'description', 'addressDescription']:
                for lang in languages:
                    lang_key = f'{key}{lang}'
                    if data_dict['language'] == lang:
                        data_dict[lang_key] = f'{data_dict[key]}'
                    else:
                        # AI translations goes here
                        tokenizer.src_lang = ai_languages_codes[data_dict['language']]
                        encoded_lang = tokenizer(data_dict[key], return_tensors="pt")
                        generated_tokens = model.generate(
                            **encoded_lang,
                            forced_bos_token_id=tokenizer.lang_code_to_id[ai_languages_codes[lang]]
                        )
                        data_dict[lang_key] = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]

            data_dict = self.delete_unused_fields(data_dict)

            return data_dict

        except KeyError as key_error:
            return {'error': f'Missing key: {str(key_error)}'}
        except ValueError as value_error:
            return {'error': f'Invalid JSON data: {str(value_error)}'}

    def delete_unused_fields(self, data_dict):
        """Delete unused fields"""
        if 'language' in data_dict:
            del data_dict['language']
        if 'title' in data_dict:
            del data_dict['title']
        if 'description' in data_dict:
            del data_dict['description']
        if 'addressDescription' in data_dict:
            del data_dict['addressDescription']

        return data_dict
