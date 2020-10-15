from flask import Flask
from flask import request
from flask import jsonify

from src.modules.functions import get_local_ranking

app = Flask(__name__)

@app.route('/ranking', methods=['POST'])
def get_ranking():
    if request.method == 'POST':
        request_json = request.json
        required = (
            'keys')
        if not all(k in request_json for k in required):
            return jsonify({'message': 'missing values'}), 400

        is_ranked = get_local_ranking(
            request_json['keys']
        )

        if not is_ranked:
            return jsonify({'message': 'fail'}), 400
        return jsonify({'message': 'success', 'result': is_ranked}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)