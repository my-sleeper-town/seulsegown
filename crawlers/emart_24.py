"""
Retrieves the address and jumpo name of emart 24 stores in Seoul from emart24.co.kr.
@returns - a list of dictionary of {jumpo_name, street_address,  latitude, longtitude}
"""
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from utils.utils import addr_to_lat_lng

def crawl_emart_24():
    '''
    서울에 있는 이마트24 점포를 찾아 반환합니다.
    반환: [{'jumpo_name': 점포이름, 'street_address': 주소, 'latitude': 위도, 'longitude': 경도}]
    '''
    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))
    driver.get("https://www.emart24.co.kr/store")
    driver.implicitly_wait(0.5)

    #시/도 드롭다운 선택
    sido = driver.find_element(By.CLASS_NAME, 'choiceVal.sido')
    ActionChains(driver).click(sido).perform()

    #서울특별시 선택
    sido_list = driver.find_element(By.CLASS_NAME, 'valueList.sidoList')
    city = sido_list.find_elements(By.TAG_NAME, 'li')
    seoul = city[9]
    ActionChains(driver).click(seoul).perform()

    #검색 버튼 선택
    search_btn = driver.find_element(By.CLASS_NAME, 'searchBtn')
    ActionChains(driver).click(search_btn).perform()

    loc_list =[] #{jumpo_name, street_address, latitude, longtitude}
    next_btn = driver.find_element(By.CLASS_NAME, 'next')    #하단 다음페이지 버튼
    idx = driver.find_element(By.CLASS_NAME, 'pIndex.focus')    #현재 페이지
    prev = int(idx.text)
    time.sleep(1)
    tmp = 0

    while prev != tmp:  #다음 페이지 버튼 선택했음에도 페이지 변화 없으면 break
        try:
            prev = tmp
            address_list = driver.find_elements(By.CLASS_NAME, "place")
            jumponame_list = driver.find_element(By.CLASS_NAME, "searchResultList").find_elements(By.CLASS_NAME, "title")
            time.sleep(1)

            for street_address, jumpo_name in zip(address_list, jumponame_list):
                lat = 0
                lng = 0
                latlng_address = addr_to_lat_lng(street_address.text)
                if latlng_address is not None:
                    try:
                        lng = latlng_address[0]
                        lat = latlng_address[1]
                    except IndexError as e:
                        print(f"Error occurred while extracting latitude and longitude from address {street_address.text}: {e}")
                        pass

                loc_list.append(
                            {
                                'jumpo_name':jumpo_name.text,
                                'street_address':street_address.text,
                                'latitude': lat, # 위도 
                                'longitude': lng  # 경도
                            }
                            )
            ActionChains(driver).click(next_btn).perform()
            time.sleep(1)

            idx = driver.find_element(By.CLASS_NAME, 'pIndex.focus')
            tmp = int(idx.text)
            time.sleep(1)
        except BaseException as ex:
            break

    return loc_list
