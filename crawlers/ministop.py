'''
서울특별시에 위치한 ministop 편의점 점포의 정보를 웹 크롤링한 함수입니다.
'''
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from utils.utils import addr_to_lat_lng

def crawl_ministop():
    # 0. 미니스톱 사이트 접속하기
    jumpos_info = []
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('https://www.ministop.co.kr/MiniStopHomePage/page/index.do')
    driver.implicitly_wait(0.5)

    #  1. 매장찾기로 마우스 이벤트
    nav_menu = driver.find_element(By.XPATH, '//*[@id="header"]/div[3]/ul/li[1]/a')
    driver.execute_script('arguments[0].click();', nav_menu)


    # 2. 드롭다움 박스 선택하기
    dropdown = Select(driver.find_element(By.XPATH, '//*[@id="area1"]'))
    dropdown.select_by_value('1')
    driver.implicitly_wait(3)

    # 3. 검색 버튼 클릭
    btn = driver.find_element(By.XPATH, '//*[@id="section"]/div[3]/div/div[2]/div[2]/div[1]/a')
    driver.execute_script('arguments[0].click();', btn)


    # 4. 각 점포 정보 저장하기'
    for i in range(1, 261):
        li_element = driver.find_element(By.XPATH, f'//*[@id="section"]/div[3]/div/div[2]/div[2]/div[1]/ul/li[{i}]')
        li_lines = li_element.text.split('\n')
        name = li_lines[0]
        address = li_lines[1]

        print(address)

        # 위도 경도 가져오는 부분
        lat = 0
        lng = 0
        latlng_address = addr_to_lat_lng(address)
        if latlng_address is not None:
            try:
                lng = latlng_address[0]
                lat = latlng_address[1]
            except IndexError as e:
                print(f'Error occurred while extracting latitude and longitude from address {address}: {e}')

        print(lat, lng)

        jumpos_info.append({
            'jumpo_name': name, 
            'street_address' : address, 
            'latitude': lat, # 위도 
            'longitude': lng, # 경도
        })

    return jumpos_info
