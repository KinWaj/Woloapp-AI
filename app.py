from flask import Flask, request, jsonify

app = Flask(__name__)


def translate_json(json_data):
    try:
        data_dict = dict(json_data)

        languages = ['pl', 'eng', 'ru', 'uk']

        for key in ['title', 'description', 'address_description']:
            for lang in languages:
                lang_key = f'{key}_{lang}'
                if data_dict['language'] == lang:
                    data_dict[lang_key] = f'{data_dict[key]}_original'
                else:
                    # AI translations goes here
                    data_dict[lang_key] = f'{data_dict[key]}_{lang}_modified'

        if 'language' in data_dict:
            del data_dict['language']
        if 'title' in data_dict:
            del data_dict['title']
        if 'description' in data_dict:
            del data_dict['description']
        if 'address_description' in data_dict:
            del data_dict['address_description']

        return data_dict

    except Exception as e:
        return {'error': str(e)}


@app.route('/translate', methods=['POST'])
def translate_json_receiver():
    try:
        received_json = request.json

        translated_data_dict = translate_json(received_json)

        return jsonify(translated_data_dict)

    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
