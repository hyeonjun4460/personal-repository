from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import certifi
from pymongo import MongoClient

ca = certifi.where()
app = Flask(__name__)

client = MongoClient('mongodb+srv://test:sparta@cluster0.qp6oa.mongodb.net/Cluster0?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.dbsparta  # mongodb atlas 내 프로젝트명

# JWT 토큰을 만들 때 필요한 비밀문자열입니다. 아무거나 입력해도 괜찮습니다.
# 이 문자열은 서버만 알고있기 때문에, 내 서버에서만 토큰을 인코딩(=만들기)/디코딩(=풀기) 할 수 있습니다.
SECRET_KEY = 'SPARTA'

# JWT 패키지를 사용합니다. (설치해야할 패키지 이름: PyJWT)
import jwt

# 토큰에 만료시간을 줘야하기 때문에, datetime 모듈도 사용합니다.
import datetime

# 회원가입 시엔, 비밀번호를 암호화하여 DB에 저장해두는 게 좋습니다.
# 그렇지 않으면, 개발자(=나)가 회원들의 비밀번호를 볼 수 있으니까요.^^;
import hashlib


#################################
##  HTML을 주는 부분             ##
#################################
@app.route('/main')
def home():
    token_receive = request.cookies.get('mytoken')
    menus = [
        {'menu': '순대국밥', 'img': '/static/sundae_soup.jpg'},
        {'menu': '소머리국밥', 'img': '/static/cow_soup.jpg'},
        {'menu': '굴국밥', 'img': '/static/oyster_soup.jpg'},
        {'menu': '돼지국밥', 'img': '/static/pork_soup.jpg'},
        {'menu': '따로국밥', 'img': '/static/separate_soup.jpg'},
        {'menu': '콩나물국밥', 'img': '/static/bean_soup.jpg'},
        {'menu': '평양온반', 'img': '/static/onban_soup.jpg'},
        {'menu': '수구레국밥', 'img': '/static/sugure_soup.jpg'},
    ]

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template('main.html', nickname=user_info["nick"], menu_list=menus)
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))


@app.route('/detail/<keyword>')
def detail(keyword):
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({'id': payload['id']})
        user_address = user_info['address']
        menu = keyword
        return render_template('detail.html', menu=menu, nickname=user_info['nick'],
                               user_address=user_address)  # 프로젝트  파일 내 html파일을 서버에 불러오고, 호출하기
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@app.route('/register')
def register():
    return render_template('register.html')


#################################
##  로그인을 위한 API            ##
#################################

# [회원가입 API]
# id, pw, nickname을 받아서, mongoDB에 저장합니다.
# 저장하기 전에, pw를 sha256 방법(=단방향 암호화. 풀어볼 수 없음)으로 암호화해서 저장합니다.
@app.route('/api/register', methods=['POST'])
def api_register():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    pw2_receive = request.form['pw2_give']
    nickname_receive = request.form['nickname_give']
    address_receive = request.form['address_give']
    gender_receive = request.form['gender_give']
    print(id_receive, pw_receive, pw2_receive, nickname_receive, address_receive, gender_receive)

    if pw_receive != pw2_receive:
        return jsonify({'result': 'pw_error', 'msg': '비밀번호가 다릅니다'})
    else:
        pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
        # db에서 입력된 아이디를 탐색
        result = db.user.find_one({'id': id_receive})
        # db에서 입력된 아이디가 탐색될 경우, alert/ 없는 경우, db에 저장하고 alert
        # ID 중복 확인 버튼
        if result is not None:
            return jsonify({'result': 'fail', 'msg': '중복된 아이디가 있습니다.'})
        # 찾지 못하면
        else:
            db.user.insert_one({'id': id_receive, 'pw': pw_hash, 'nick': nickname_receive, 'address': address_receive,
                                'gender': gender_receive})
            return jsonify({'result': 'success', 'msg': '회원가입을 완료했습니다.'})


# register 중 id 중복 확인
@app.route('/api/register/id', methods=['POST'])
def api_register_id():
    id_receive = request.form['id_give']
    print(id_receive)
    # db에서 입력된 아이디를 탐색
    result = db.user.find_one({'id': id_receive})

    # db에서 입력된 아이디가 탐색될 경우, alert/ 없는 경우, db에 저장하고 alert

    # ID 중복 확인 버튼
    if id_receive == '':
        return jsonify({'result': 'empty', 'msg': '아이디를 입력해주세요.'})
    elif result is not None:
        return jsonify({'result': 'fail', 'msg': '중복된 아이디가 있습니다.'})
    # 찾지 못하면
    else:
        return jsonify({'id': id_receive, 'result': 'success', 'msg': '사용 가능한 아이디입니다.'})


@app.route('/api/register/pw', methods=['POST'])
def api_register_pw():
    id_receive = request.form['id_give']
    print(id_receive)
    # db에서 입력된 아이디를 탐색
    result = db.user.find_one({'id': id_receive})

    # db에서 입력된 아이디가 탐색될 경우, alert/ 없는 경우, db에 저장하고 alert

    # ID 중복 확인 버튼
    if id_receive == '':
        return jsonify({'result': 'empty', 'msg': '아이디를 입력해주세요.'})
    elif result is not None:
        return jsonify({'result': 'fail', 'msg': '중복된 아이디가 있습니다.'})
    # 찾지 못하면
    else:
        return jsonify({'id': id_receive, 'result': 'success', 'msg': '사용 가능한 아이디입니다.'})


# [로그인 API]
# id, pw를 받아서 맞춰보고, 토큰을 만들어 발급합니다.
@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    # 회원가입 때와 같은 방법으로 pw를 암호화합니다.
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    # id, 암호화된pw을 가지고 해당 유저를 찾습니다.
    result = db.user.find_one({'id': id_receive, 'pw': pw_hash})
    print(result)

    # 찾으면 JWT 토큰을 만들어 발급합니다.
    if id_receive == '':
        return jsonify({'result': 'fail_id', 'msg': '아이디를 입력해주세요.'})
    elif pw_receive == '':
        return jsonify({'result': 'fail_pw', 'msg': '비밀번호를 입력해주세요.'})
    elif result is not None:
        # JWT 토큰에는, payload와 시크릿키가 필요합니다.
        # 시크릿키가 있어야 토큰을 디코딩(=풀기) 해서 payload 값을 볼 수 있습니다.
        # 아래에선 id와 exp를 담았습니다. 즉, JWT 토큰을 풀면 유저ID 값을 알 수 있습니다.
        # exp에는 만료시간을 넣어줍니다. 만료시간이 지나면, 시크릿키로 토큰을 풀 때 만료되었다고 에러가 납니다.
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=300)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        # token을 줍니다.
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디와 비밀번호를 확인해주세요.'})


# 회원별 리뷰 POST 기능: 리뷰, 회원의 닉네임 가져오기
@app.route('/detail/<keyword>/recipe', methods=['POST'])
def post_review(keyword):
    menu_receive = request.form['menu_give']
    nick_receive = request.form['nick_give']
    comment_receive = request.form['comment_give']
    doc = {
        'menu': menu_receive,
        'nick_receive': nick_receive,
        'comment_receive': comment_receive
    }
    db.recipe_comment.insert_one(doc)
    return jsonify({'msg': '나만의 레시피를 등록 완료.'})


@app.route('/detail/<keyword>/recipe', methods=['GET'])
def get_review(keyword):
    menu = keyword
    recipe_list = list(db.recipe_comment.find({'menu': menu}, {'_id': False}))
    if (len(recipe_list) == 0):
        return jsonify({'result': 'empty', 'msg': 'There is no recipe in this menu. Sorry...'})
    else:
        return jsonify({'result': 'success', 'recipe_list': recipe_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
