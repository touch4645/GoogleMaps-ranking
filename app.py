from flask import Flask
from flask import request
from flask import jsonify

from src.modules.functions import get_local_ranking
from src.modules.Google_Ads import get_keywords_data
from src.modules.functions import get_keyword_relation

import logging
import sys


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


# ログを標準出力に出力する
app.logger.addHandler(logging.StreamHandler(sys.stdout))
# （レベル設定は適宜行ってください）
app.logger.setLevel(logging.INFO)


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
            app.logger.info(jsonify({'message': 'missing values'}))
            return jsonify({'message': 'missing values'}), 400

        is_ranked = get_local_ranking(
            request_json['keys'], request_json['address']
        )

        if not is_ranked:
            app.logger.info(jsonify({'message': 'fail'}))
            return jsonify({'message': 'fail'}), 400
        app.logger.info(jsonify({'message': 'success', 'result': is_ranked}))
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
            app.logger.info(jsonify({'message': 'missing values'}))
            return jsonify({'message': 'missing values'}), 400

        customer_id = DEFAULT_CUSTOMER_ID
        language_id = DEFAULT_LANGUAGE_ID
        location_id = DEFAULT_LOCATION_ID

        if 'keys' in request_json:
            keyword = request_json['keys']
        else:
            keyword = ''

        if 'page_url' in request_json:
            page_url = request_json['page_url']
        else:
            page_url = ''

        is_volumed = get_keywords_data(
            customer_id, location_id, language_id, keyword, page_url
        )

        if not is_volumed:
            app.logger.info(jsonify({'message': 'fail'}))
            return jsonify({'message': 'fail'}), 400
        app.logger.info(jsonify({'message': 'success', 'result': is_volumed}))
        return jsonify({'message': 'success', 'result': is_volumed}), 201


@app.route('/relation', methods=['POST'])
def get_relational_keywords():
    if request.method == 'POST':
        request_json = request.json

        if not 'keys' in request_json:
            app.logger.info(jsonify({'message': 'missing values'}))
            return jsonify({'message': 'missing values'}), 400

        is_related = get_keyword_relation(request_json['keys'])

        if not is_related:
            app.logger.info(jsonify({'message': 'fail'}))
            return jsonify({'message': 'fail'}), 400
        app.logger.info(jsonify({'message': 'success', 'result': is_related}))
        return jsonify({'message': 'success', 'result': is_related}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)