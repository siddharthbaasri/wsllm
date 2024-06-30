import requests
import json
import os
from helpers import headers

def getSearchJSON(query):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": os.getenv('GOOGLE_SEARCH_API_KEY'),
        'cx': os.getenv('GOOGLE_SEARCH_ENGINE_ID'),
        'q': query + ' site:uw.edu OR site:washington.edu',
        'num': 5
    }
    
    try:
        response = requests.get(url, headers = headers, params = params)
        JSONresponse = json.loads(response.text)
        return [{'title': item['title'], 'url': item['link']} for item in JSONresponse['items']]
    except:
        return []