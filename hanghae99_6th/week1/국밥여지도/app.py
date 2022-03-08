from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


# 메인 페이지 서버 만들기
@app.route('/')
def home():
    menus = [
        '순대국밥',
        '소머리국밥',
        '굴국밥',
        '돼지국밥',
        '따로국밥',
        '콩나물국밥',
        '평양온반',
        '수구레국밥']
    print(menus)
    return render_template('main.html', menus=menus)  # 프로젝트  파일 내 html파일을 서버에 불러오고, 호출하기


@app.route('/detail/<keyword>')
def sample(keyword):
    menu = keyword
    return render_template('detail.html', menu=menu)  # 프로젝트  파일 내 html파일을 서버에 불러오고, 호출하기


@app.route('/prac')
def prac():
    return render_template('index_prac.html')  # 프로젝트  파일 내 html파일을 서버에 불러오고, 호출하기


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
