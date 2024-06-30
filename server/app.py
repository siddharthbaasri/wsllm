from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
from websearch import Websearch

app = Flask(__name__)
load_dotenv()
search_client = Websearch()

@app.route("/search")
def get_search_results():
    queryString = request.args.get('q')
    llm_response = search_client.search(queryString)
    return llm_response