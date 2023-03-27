from flask import Flask, request
from flask_cors import CORS
from andromeda.ranker import BM25

from api.utils import get_metadata


def run():
    app = Flask(__name__)
    CORS(app)

    @app.route('/', methods=['GET'])
    def index():
        return "Welcome to Andromeda's API"

    @app.route('/search', methods=['GET'])
    def search():
        query = request.args['query']

        ranker = BM25()
        results = ranker.get_docs(query)

        page = int(request.args['page']) - 1 if 'page' in request.args else 0
        per_page = int(request.args['per_page']) if 'per_page' in request.args else len(results)
        first = page * per_page
        last = first + per_page

        return results[first:last]

    @app.route('/metadata', methods=['GET'])
    def metadata():
        url = request.args['url']

        return get_metadata(url)

    return app
