from flask import Flask, jsonify, request
from dotenv import load_dotenv
from websearch import Websearch
from flask_cors import CORS

app = Flask(__name__)
load_dotenv()
CORS(app)
search_client = Websearch()

@app.route("/search")
def get_search_results():
    queryString = request.args.get('q')
    searchData = search_client.search(queryString)
    return jsonify({'llmResponse': searchData[0], 'links': searchData[1]})