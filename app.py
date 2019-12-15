from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('index.html')

@app.route('/order', methods=['GET'])
def getting():
    # 모든 document 찾기 & _id 값은 출력에서 제외하기
    result = list(db.orders.find({},{'_id':0}))
    # articles라는 키 값으로 영화정보 내려주기
    return jsonify({'result':'success', 'orders':result})

@app.route("/order", methods=["POST"])
def saving():

    name = request.form.get("Name")
    number = request.form.get("Count")
    address = request.form.get("Address")
    phone = request.form.get("Phone")


    order = {
        'name_give' :name,
        'number_give' :number,
        'address_give' :address,
        'phone_give' :phone
    }

    # mongoDB에 넣는 부분

    db.orders.insert_one(order)

    return jsonify({'result':'success'})

if __name__ == '__main__':
   app.run('127.0.0.1',port=5000,debug=True)