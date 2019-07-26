import sys
import urllib.request
import requests
import json
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import json
import collections


def weather(name):
    url = 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query='+name
    req = requests.get(url)
    html = req.text
    bs = BeautifulSoup(html, 'html.parser')
    temp = bs.find('p', attrs={'class': 'info_temperature'})
    info = bs.find('ul', attrs={'class': 'info_list'})
    value = {'temp': temp.getText(), 'info': info.getText() }
    # obj = collections.OrderedDict(value)
    # jsonData = json.dumps(obj, ensure_ascii=False, sort_keys=False)

    return str(name) +":" +value['temp'] +","+ "\n세부날씨" +":"+ value['info']
    #v = { "messages": [{"speech": "Text response","type": 0}] }
    #return v

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/', methods=['POST', 'GET'])
def webhook():
    #content = request.args.get('geo-city')
    a = request.get_json()
    value = a['queryResult']['parameters']['geo-city']
    #return weather(value+"날씨")
    #return { "status" : "success" }
    a['fulfillmentText'] = weather(value+"날씨")
    return a

if __name__ == '__main__':
    app.run(host='0.0.0.0')
