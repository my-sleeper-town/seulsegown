#/usr/bin/env python
"""
Retrieves the address and jumpo name of 7-Eleven stores in Seoul from 7-Eleven.co.kr.
@returns - a list of pairs of (jumpo_name, street_address)
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from utils.utils import addr_to_lat_lng

URL = 'https://www.7-eleven.co.kr/'

def crawl_seven_eleven():
    '''
    서울에 있는 세븐일레븐 점포를 찾아 반환합니다.
    반환: [{'jumpo_name': 점포이름, 'street_address': 주소, 'latitude': 위도, 'longitude': 경도}]
    '''
    jumpos = []
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('https://www.7-eleven.co.kr/')

    # 점포찾기 버튼 클릭
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//a[@href="/util/storeLayerPop.asp"]')))
    store_open = driver.find_element(By.XPATH, '//a[@href="/util/storeLayerPop.asp"]')
    store_open.click()

    # 시/도 선택 드롭다운메뉴
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'storeLaySido')))
    storeLaySido = Select(driver.find_element(By.ID, 'storeLaySido'))
    storeLaySido.select_by_value("서울")

    # 구 선택 드롭다운메뉴
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'storeLayGu')))
    WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, '//select[@id="storeLayGu"]/option')))
    storeLayGu = Select(driver.find_element(By.ID, 'storeLayGu'))
    storeButton1 = driver.find_element(By.ID, 'storeButton1')

    options = [option.get_attribute('value') for option in storeLayGu.options][1:]

    for option in options:
        # 매번 다시 선택해줘야함
        WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.ID, 'layer')))
        WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.ID, 'storeLayGu')))
        WebDriverWait(driver, 40).until(EC.presence_of_all_elements_located((By.XPATH, '//select[@id="storeLayGu"]/option')))
        storeLayGu = Select(driver.find_element(By.ID, 'storeLayGu'))
        storeButton1 = driver.find_element(By.ID, 'storeButton1')

        storeLayGu.select_by_value(option)
        storeButton1.click()

        WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.ID, 'layer')))
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="list_stroe"]/ul/li/a')))
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))
        sleep(10)
        jumpo_links = driver.find_elements(By.XPATH, '//div[@class="list_stroe"]/ul/li/a')

        for jumpo in jumpo_links:
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="list_stroe"]/ul/li/a/span')))
            jumpo_name = jumpo.find_element(By.XPATH, './span[1]').text.strip()
            address = jumpo.find_element(By.XPATH, './span[2]').text.strip()

            lng_lat = addr_to_lat_lng(address)

            jumpos.append(
                {
                    "jumpo_name": jumpo_name,
                    "street_address": address,
                    "latitude": lng_lat[0] if lng_lat else 0,
                    "longitude": lng_lat[1] if lng_lat else 0,
                }
            )
 
    driver.quit()
    return jumpos