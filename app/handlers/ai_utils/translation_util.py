"""AI Utils tool for translations"""

from transformers import pipeline


class TranslationTool:
    def __init__(self, fields_to_translate):
        self.translation_pipe = pipeline("translation", model="facebook/mbart-large-50-many-to-many-mmt")
        self.languages = ['PL', 'EN', 'UA', 'RU']
        self.ai_languages_codes = {'PL': 'pl_PL', 'EN': 'en_XX', 'UA': 'uk_UA', 'RU': 'ru_RU'}
        self.fields_to_translate = fields_to_translate

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
