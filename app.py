import os
import sys
import urllib.request
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup
import json

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

##HTML 주는 부분
@app.route('/')
def home():
   return render_template('HOME.html')

@app.route('/searching')
def searching():
   return render_template('도서검색.html')

@app.route('/index')
def index():
   return render_template('등록도서목록.html')

@app.route('/analysis')
def analysis():
   return render_template('독서경향분석.html')

@app.route('/searching1', methods=['GET'])
def searching1():

    client_id = "4HH71ddS9UsMNwN22tlW"
    client_secret = "Vp0TaRotzG"

    #도서검색 url
    title = request.args.get('book_name')

    encText = urllib.parse.quote(title)
    url = 'https://openapi.naver.com/v1/search/book.json?query=' + encText

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }

    # mongoDB에 넣는 부분
    data = requests.get(url, headers=headers)
    json_data = data.json()
    json_data_new = json_data['items']

    db.books.insert(json_data_new)

    collection = db.books
    results = collection.find()

    return render_template('도서검색.html',data=results)

if __name__ == '__main__':
   app.run('127.0.0.1',port=5000,debug=True)