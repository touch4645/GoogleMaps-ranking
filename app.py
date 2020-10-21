from flask import Flask
from flask import request
from flask import jsonify

from src.modules.functions import get_local_ranking
from src.modules.Google_Ads import get_keywords_data

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/ranking', methods=['POST'])
def get_ranking():
    if request.method == 'POST':
        request_json = request.json
        required = (
            'keys', 'address')
        if not all(k in request_json for k in required):
            return jsonify({'message': 'missing values'}), 400

        is_ranked = get_local_ranking(
            request_json['keys'], request_json['address']
        )

        if not is_ranked:
            return jsonify({'message': 'fail'}), 400
        return jsonify({'message': 'success', 'result': is_ranked}), 201


# test account id
DEFAULT_CUSTOMER_ID = '5566257480'
# Japanese id
DEFAULT_LANGUAGE_ID = '1005'
# Japan id
DEFAULT_LOCATION_ID = ['2392']


@app.route('/volume', methods=['POST'])
def get_volume():
    if request.method == 'POST':
        request_json = request.json
        required = (
            'keys', 'page_url')
        if not any(k in request_json for k in required):
            return jsonify({'message': 'missing values'}), 400

        customer_id = DEFAULT_CUSTOMER_ID
        language_id = DEFAULT_LANGUAGE_ID
        location_id = DEFAULT_LOCATION_ID

        keyword = []
        if 'keys' in request_json:
            keyword.append(request_json['keys'])

        if 'page_url' in request_json:
            page_url = request_json['page_url']
        else:
            page_url = ''

        is_volumed = get_keywords_data(
            customer_id, location_id, language_id, keyword, page_url
        )

        if not is_volumed:
            return jsonify({'message': 'fail'}), 400
        return jsonify({'message': 'success', 'result': is_volumed}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)