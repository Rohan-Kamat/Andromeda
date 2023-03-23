from flask import Flask, request

from andromeda.ranker import BM25


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "Welcome to Andromeda's API"

@app.route('/search', methods=['GET'])
def search():
    query = request.args['query']
    ranker = BM25()
    return ranker.get_docs(query)
