from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
#import csv

def crawling():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.ministop.co.kr/MiniStopHomePage/page/index.do")
    driver.implicitly_wait(0.5)


    ''' 1. 매장찾기로 마우스 이벤트 '''
    nav_menu = driver.find_element(By.XPATH, '//*[@id="header"]/div[3]/ul/li[1]/a')
    # button = driver.find_element(By.CLASS_NAME, "nav001")
    # ActionChains(driver).click(button).perform()

    # 해결 1(성공)
    driver.execute_script("arguments[0].click();", nav_menu)

    # 해결 2(실패)
    # ActionChains(driver).move_to_element(button).click().perform()

    '''2. 드롭다움 박스 선택하기'''
    dropdown = Select(driver.find_element(By.XPATH, '//*[@id="area1"]'))
    dropdown.select_by_value("1")
    driver.implicitly_wait(3)
    # 검색 버튼 클릭
    btn = driver.find_element(By.XPATH, '//*[@id="section"]/div[3]/div/div[2]/div[2]/div[1]/a')
    driver.execute_script("arguments[0].click();", btn)


    '''3. 가져온 텍스트 파일을 csv파일에 저장'''

    # csv 파일 생성
    #filename = '/Users/suyoung/Desktop/output.csv'
    #with open(filename, 'w', encoding='utf-8', newline='') as f:
    #    writer = csv.writer(f)
    #    writer.writerow(['name', 'address', 'phone'])

    #cate = Category(category_name='편의점').save()
    #brd = Brand(brand_id = )

    test_list = [] 
    for i in range(1, 261):
        li_element = driver.find_element(By.XPATH, f'//*[@id="section"]/div[3]/div/div[2]/div[2]/div[1]/ul/li[{i}]')
        li_lines = li_element.text.split('\n')
        name = li_lines[0]
        address = li_lines[1]
        phone = li_lines[2]

        print(name)
        print(address)
        print(phone)

        # csv 파일에 추가
        #writer.writerow([name, address, phone])



def main():
    crawling()


if __name__ == "__main__":
    main()