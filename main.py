from flask import Flask
from flask_restful import reqparse , Api ,Resource
from bs4 import BeautifulSoup
import pymysql
import sys
import io
import urllib.request
import requests
import json
import collections
from flask_cors import CORS

app = Flask(__name__)
api = CORS(app)
app.config['CORS_HEADERS'] = 'application/json'
api = Api(app)

sys.stdout = io.TextIOWrapper(sys.stdout.detach(),encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(),encoding='utf-8')
conn = pymysql.connect(host='35.206.122.211', user='root', password='djemals',db = 'test', charset='utf8')
curs = conn.cursor()

@app.route("/")
def defaultPage():
    return "<h1>Welcome to D3Project API<h1>"

@app.route("/search/<title>", methods=['GET'])
def search(title):
    client_id = "keEC3LAFtPejhNUY5Dh4"
    client_secret = "gpbNkH23IT"
    encText = urllib.parse.quote(title)
    url = "https://openapi.naver.com/v1/search/blog?query=" + encText  # json 결과
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if (rescode == 200):
        response_body = response.read()
        return response_body.decode('utf-8')

@app.route("/review/<name>", methods=['GET'])
def review(name):
    url = 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query='+name
    req = requests.get(url)
    html = req.text
    bs = BeautifulSoup(html, 'html.parser')
    img = bs.findAll('img', attrs={'class': 'sh_blog_thumbnail'})
    _title = bs.findAll('a', attrs={'class': 'sh_blog_title _sp_each_url _sp_each_title'})
    # passage = bs.findAll('dd', attrs={'class': 'sh_blog_passage'})
    value = {
        'count':"3",
        'item': [
            {'title': _title[0]['title'], 'img': img[0]['src']},
            {'title': _title[1]['title'], 'img': img[1]['src']},
            {'title': _title[2]['title'], 'img': img[2]['src']}
        ]
    }
    obj = collections.OrderedDict(value)
    jsonData = json.dumps(obj, ensure_ascii=False, sort_keys=False)
    return jsonData

@app.route("/signup", methods=['GET'])
def Userdata():
    sql = "select * from test1"
    curs.execute(sql)
    rows = curs.fetchall() 
    value = {}
    l = []
    for a in rows:
        l.append(a)
    value['people'] = l
    obj = collections.OrderedDict(value)
    jsonData = json.dumps(obj, ensure_ascii=False, sort_keys=False)
    return jsonData

class CreateUser(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str)
            parser.add_argument('age', type=str)
            args = parser.parse_args()
            _userName = args['name']
            _userAge= args['age']
            sql5 = "insert into test1(name,age) values('"+_userName+"',"+_userAge+")"
            curs.execute(sql5)
            conn.commit()
            return { 'Status' : 'Success' }
        except Exception as e:
            return {'error': str(e)}

api.add_resource(CreateUser, '/user')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
