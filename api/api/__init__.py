from flask import Flask, request

from andromeda.ranker import BM25

from api.utils import get_metadata


def run():
    app = Flask(__name__)

    @app.route('/', methods=['GET'])
    def index():
        return "Welcome to Andromeda's API"

    @app.route('/search', methods=['GET'])
    def search():
        query = request.args['query']
        detailed = True if 'detailed' in request.args else False

        ranker = BM25()
        results = ranker.get_docs(query)[:5]

        if detailed:
            results = [get_metadata(url) for url in results]

        return results

    return app
