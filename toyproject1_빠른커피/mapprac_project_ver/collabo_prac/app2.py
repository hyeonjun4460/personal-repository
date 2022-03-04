from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException
from bs4 import BeautifulSoup
from time import sleep
from selenium.common.exceptions import TimeoutException

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')  # 프로젝트  파일 내 html파일을 서버에 불러오고, 호출하기


@app.route("/data", methods=["POST"])
def get_search():
    wrap = []
    search_receive = request.form['search_give']
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('lang=ko_KR')
    chromedriver_path = 'C:/Users/hyeon/OneDrive/문서/sparta/toys/collabo_hard/chromedriver.exe'
    driver = webdriver.Chrome(chromedriver_path, options=options)  # chromedriver 열기

    def main():
        driver.implicitly_wait(4)  # 렌더링 될때까지 기다린다 4초
        driver.get('https://map.kakao.com/')  # 주소 가져오기

        search(search_receive)
        driver.quit()
        print("finish")
        # return c

    def search(place):

        search_area = driver.find_element(By.XPATH, '//*[@id="search.keyword.query"]')
        search_area.send_keys(place)  # 검색어 입력
        driver.find_element(By.XPATH, '// *[ @ id = "search.keyword.submit"]').send_keys(Keys.ENTER)  # Enter로 검색
        sleep(1)

        # 검색된 정보가 있는 경우에만 탐색
        # 1번 페이지 place list 읽기
        html = driver.page_source

        soup = BeautifulSoup(html, 'html.parser')
        place_lists = soup.select('.placelist > .PlaceItem')  # 검색된 장소 목록

        # 검색된 첫 페이지 장소 목록 크롤링하기
        crawling(place_lists)
        search_area.clear()
        # print(b)
        # return b

    def crawling(placeLists):
        # 광고배너는 건너 뛰고 목록 상세보기 클릭하기
        for i, place in enumerate(placeLists):
            if i == 3:
                continue
            else:
                searchMenuInfo(i)
                wrap.append(searchMenuInfo(i))
        return wrap

    def searchMenuInfo(i):
        # 상세페이지로 가서 메뉴찾기
        global soup
        menuInfos = []
        detail_page_xpath = '//*[@id="info.search.place.list"]/li[' + str(i + 1) + ']/div[5]/div[4]/a[1]'
        driver.find_element(By.XPATH, detail_page_xpath).send_keys(Keys.ENTER)
        driver.switch_to.window(driver.window_handles[-1])  # 상세정보 탭으로 변환
        sleep(1)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # 메뉴의 3가지 타입
        menuonlyType = soup.select('.cont_menu > .list_menu > .menuonly_type')
        nophotoType = soup.select('.cont_menu > .list_menu > .nophoto_type')
        photoType = soup.select('.cont_menu > .list_menu > .photo_type')

        if len(menuonlyType) != 0:
            menuInfos.append(getTitle())
            for menu in menuonlyType:
                menuInfos.append(getMenuInfo(menu))

        elif len(nophotoType) != 0:
            menuInfos.append(getTitle())
            for menu in nophotoType:
                menuInfos.append(getMenuInfo(menu))
        else:
            menuInfos.append(getTitle())
            for menu in photoType:
                menuInfos.append(getMenuInfo(menu))

        driver.close()
        driver.switch_to.window(driver.window_handles[0])  # 검색 탭으로 전환하는 것

        return menuInfos

    def getMenuInfo(menu):
        menuName = menu.select('.info_menu > .loss_word')[0].text
        menuPrices = menu.select('.info_menu > .price_menu')
        menuPrice = ''

        if len(menuPrices) != 0:
            menuPrice = menuPrices[0].text.split(' ')[1]
        else:
            menuPrice = '가격정보없음'

        return dict(menu=menuName, price=menuPrice)

    def getTitle():
        titleName = soup.find('title').text.split('|')[0]
        titleAddress = soup.select(
            '.cont_essential > .details_placeinfo > .placeinfo_default > .location_detail > .txt_address')
        for shopaddress in titleAddress:
            address = shopaddress.text.replace(' ', '').replace('\n', '').strip()

        return dict(shopname=titleName, shopaddress=address)

    main()
    return jsonify({'data': wrap})


if __name__ == "__main__":
    app.run('0.0.0.0', port=5000, debug=True)
