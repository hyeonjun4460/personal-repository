from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.6dpq9.mongodb.net/Cluster0?retryWrites=true&w=majority',  tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')


@app.route("/cheers", methods=["POST"])
def cheers_post():
    nickname_receive = request.form['nickname_give']
    comments_receive = request.form['comment_give']
    count = list(db.fanpage.find({},{'_id': False}))
    num = len(count)
    doc = {
        'nickname': nickname_receive,
        'comment': comments_receive,
        'num': num
    }
    db.fanpage.insert_one(doc)
    return jsonify({'msg': '입력 완료'})

@app.route("/cheers", methods=["GET"])
def cheers_get():
    cheers_list = list(db.fanpage.find({},{'_id': False}))
    return jsonify({'cheer_list':cheers_list})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
