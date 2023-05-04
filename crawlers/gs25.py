#/usr/bin/env python
"""
Retrieves the address and jumpo name of GS25 stores in Seoul from "gs25.gsretail.com/gscvs/ko/store-services/locations"
@returns - a list of dictionary of {'jumpo_name': '', 
                                    'street_address': '', 
                                    'latitude': '', 
                                    'longitude': ''}    
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from utils.utils import addr_to_lat_lng
from time import sleep

def crawl_gs25():
    '''
    서울에 있는 GS25 점포를 찾아 반환합니다.
    반환: [{'점포이름': , '점포주소': , '위도': , '경도': }] 형식의 딕셔너리 리스트 
    '''
    jumpos = []
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('http://gs25.gsretail.com/gscvs/ko/store-services/locations')
    
    ## 지역선택 combo box를 클릭 후 서울시 클릭
    seoul_select = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'stb1')))
    seoul_select = Select(seoul_select)
    seoul_select.select_by_visible_text('서울시')
    
    ## 검색 버튼을 클릭 (검색 버틀을 누를 시 화면에 서울시 매장 정보가 나옴)
    driver.find_element(By.ID, 'searchButton').click()
    sleep(5)

    current_page = 1
    while current_page <= 623:
        jumpo_links = driver.find_elements(By.XPATH, '//tbody[@id="storeInfoList"]/tr')
        for jumpo in jumpo_links:
            jumpo_name = WebDriverWait(jumpo, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'st_name'))).text
            address = WebDriverWait(jumpo, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'st_address'))).text
            lat = 0
            lng = 0
            latlng_address = addr_to_lat_lng(address)
            if latlng_address is not None:
                try:
                    lng = latlng_address[0]
                    lat = latlng_address[1]
                except IndexError as e:
                    print(f"Error occurred while extracting latitude and longitude from address {address}: {e}")
                    pass
            jumpos.append(
                {
                    'jumpo_name': jumpo_name,
                    'street_address': address,
                    'latitude': lat,
                    'longitude': lng
                }
            )
            
        ## 다음 페이지 데이터 수집을 위해 next button 클릭
        sleep(1)
        driver.find_element(By.CLASS_NAME, 'next').send_keys(Keys.ENTER)
        current_page += 1
        sleep(1)
    driver.quit()

    return jumpos