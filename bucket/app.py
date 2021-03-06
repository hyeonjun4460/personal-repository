from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.6dpq9.mongodb.net/Cluster0?retryWrites=true&w=majority',  tlsCAFile=ca)
db = client.dbshyeonjun
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form['bucket_give']
    bucket_list = list(db.buckets.find({}, {'_id': False}))
    bucket_count = len(bucket_list) + 1
    doc = {
        'num': bucket_count,
        'list': bucket_receive,
        'done': 0
    }
    db.buckets.insert_one(doc)
    return jsonify({'msg': '등록 완료'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form['num_give']
    db.buckets.update_one({'num': int(num_receive)}, {'$set': {'done': 1}})
    return jsonify({'msg': '완료!'})


@app.route("/bucket", methods=["GET"])
def bucket_get():
    bucket_list = list(db.buckets.find({}, {'_id': False}))
    return jsonify({'bucket': bucket_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
