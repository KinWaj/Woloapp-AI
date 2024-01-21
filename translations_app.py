"""Module for AI translations funtionalities"""

from flask import Flask, request, jsonify
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

app = Flask(__name__)


def translate_json(json_data):
    """Translates recieved json data with AI and returns modified dictionary.
     Creates keys for every language separately"""
    try:
        data_dict = dict(json_data)

        model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
        tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")

        # TODO - add coding for uk and ru
        languages = ['pl', 'eng']
        ai_languages_codes = {
            'pl': 'pl_PL',
            'eng': 'en_XX'
        }

        for key in ['title', 'description', 'address_description']:
            for lang in languages:
                lang_key = f'{key}_{lang}'
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

        if 'language' in data_dict:
            del data_dict['language']
        if 'title' in data_dict:
            del data_dict['title']
        if 'description' in data_dict:
            del data_dict['description']
        if 'address_description' in data_dict:
            del data_dict['address_description']

        return data_dict

    except KeyError as key_error:
        return {'error': f'Missing key: {str(key_error)}'}
    except ValueError as value_error:
        return {'error': f'Invalid JSON data: {str(value_error)}'}


@app.route('/translate', methods=['POST'])
def translate_json_receiver():
    """Receives json to translate and gives back translated version (also json)"""
    try:
        received_json = request.json

        translated_data_dict = translate_json(received_json)

        return jsonify(translated_data_dict)

    except ValueError as value_error:
        return jsonify({'error': f'Invalid JSON data: {str(value_error)}'})


if __name__ == '__main__':
    app.run(debug=True)
