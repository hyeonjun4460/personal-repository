from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 메인 페이지 서버 만들기
@app.route('/')
def home():
    return render_template('index.html')  # 프로젝트  파일 내 html파일을 서버에 불러오고, 호출하기

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
