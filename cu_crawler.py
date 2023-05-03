from collections import defaultdict
from bs4 import BeautifulSoup
import django
import requests
import os, time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seulsegown.settings")
django.setup()
from store.models import Category, Brand, Jumpo

"""
CU 편의점 목록과 주소를 가져오기 위한 함수들입니다.
CU 웹사이트는 특정 파라미터(DATA)로 POST 요청을 보내는 방식으로 동작하고 있습니다.
따라서, DATA를 전역 딕셔너리 변수로 선언하여 각 함수마다 필요한 파라미터를 변환하여 사용하고 있습니다.

작성자 : 서대원
작성일 : 2023. 5. 2.
"""

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)\
     Chrome/112.0.0.0 Safari/537.36',
}

DATA = {
    "pageIndex": 1,
    "listType": "",
    "jumpoCode": "",
    "jumpoLotto": "",
    "jumpoToto": "",
    "jumpoCash": "",
    "jumpoHour": "",
    "jumpoCafe": "",
    "jumpoDelivery": "",
    "jumpoBakery": "",
    "jumpoFry": "",
    "jumpoMultiDevice": "",
    "jumpoPosCash": "",
    "jumpoBattery": "",
    "jumpoAdderss": "",
    "jumpoSido": "서울특별시",
    "jumpoGugun": "",
    "jumpodong": "",
    "user_id": "",
    "sido": "서울특별시",
    "Gugun": "",
    "jumpoName": "",
}

URLS = {
    'gugun': 'https://cu.bgfretail.com/store/GugunList.do',
    'dong': 'https://cu.bgfretail.com/store/DongList.do',
    'jumpo': 'https://cu.bgfretail.com/store/list_Ajax.do'
}


def post_request(url, data, headers=None):
    """
    url 주소와 data, headers로 http post 요청을 보내는 함수입니다.

    Args:
        url (str): post 요청을 보낼 url 주소
        data (dict) : post 요청에 함께 보낼 각종 파라미터
        headers (dict) : post 요청에 함께 보낼 user-agent

    Returns:
        requests.Response object
    """
    return requests.post(url, data=data, headers=headers)


def get_soup(html):
    """
    파싱할 html 데이터를 인자로 받아 BeautifulSoup 객체를 리턴하는 함수입니다.
    get_jumpo_info() 함수에서 사용합니다.

    Args:
        html (str) : 파싱할 html -> requests.Response.text

    Returns:
        bs4.BeautifulSoup
    """
    return BeautifulSoup(html, 'html.parser')


def get_district_info(city):
    """
    시도명(city)을 인자로 받아 구/군명을 리스트로 받환하는 함수입니다.

    Args:
        city (str) : 요청을 보낼 시도명 예)서울특별시

    Returns:
        list -> ['강남구', '강동구', '강북구', ..., ]
    """
    DATA['jumpoSido'] = DATA['sido'] = city
    req = post_request(URLS['gugun'], data=DATA)
    return [gu['CODE_NAME'] for gu in req.json()['GugunList']]


def get_town_info(gu):
    """
    구 명(gu)을 인자로 받아 동 목록을 리스트 자료형으로 받환하는 함수입니다.

    Args:
        gu (str) : 요청을 보낼 구 명 예)강남구

    Returns:
        list -> [개포2동', '개포4동', '개포동', '논현1동', '논현2동', '논현동', ...,]
    """
    DATA['jumpoGugun'] = DATA['Gugun'] = gu
    req = post_request(URLS['dong'], data=DATA)
    return [dong['CODE_NAME'] for dong in req.json()['GugunList']]


def get_jumpo_info(gu, dong):
    """
    구 명(gu)과 동 명(dong)을 인자로 받아 점포 목록을 딕셔너리의 리스트 형태로 받환하는 함수입니다.
    점포 딕셔너리에는 점포명(jumpo_name), 도로명주소(street_address), 위도(latitude), 경도(longitude)가 포함됩니다.
    * 위도와 경도에는 임의의 값으로 서울 도심 좌표인 37.564214 / 127.001699이 들어갑니다.

    Args:
        gu (str) : 요청을 보낼 구 명 예)강남구
        dong (str) : 요청을 보낼 동 명 예)개포동

    Returns:
        list(dictionary)-> [{'jumpo_name': '중랑베스트점',
                            'jumpo_street_address': '서울특별시 중랑구 봉화산로4길 28 (중화동)',
                            'latitude': 37.564214,
                            'longitude': 127.001699 }, ..{}.. , ]
    """
    DATA['jumpoGugun'] = DATA['Gugun'] = gu
    DATA['jumpodong'] = dong
    DATA['pageIndex'] = 1
    total_store_info = []
    print(f'>>> {gu} {dong} 스크래핑을 시작합니다.')
    while True:
        req = post_request(URLS['jumpo'], data=DATA, headers=HEADERS)
        soup = BeautifulSoup(req.text, 'html.parser')
        stores = soup.select(
            '#result_search > div.result_store > div.detail_store > table > tbody > tr')
        if stores[0].find('td').text == '등록된 게시물이 없습니다.':
            print('>>> 점포가 없으므로 스크래핑하지 않습니다.')
        else:
            for store in stores:
                total_store_info.append({
                    'jumpo_name': store.find('span').text,
                    'street_address': store.find('address').text.strip(),
                    'latitude': 37.564214,
                    'longitude': 127.001699,
                })

        if soup.select('#paging > a') and soup.select('#paging > a')[-1].text != '이전':
            DATA['pageIndex'] += 1
            print('>>> 다음 페이지로 이동합니다.')
        else:
            print('>>> 다음 페이지가 없으므로 종료합니다.')
            break

    return total_store_info


def save_data(jumpo_list, category='편의점', brand='CU'):
    """
    점포 목록(jumpo_list)과 업종명(category), 브랜드명(brand)을 인자로 받아 데이터를 DB에 저장하는 함수입니다.
    * category와 brand 인자는 각각 '편의점'과 'CU'를 기본값으로 가집니다.

    Args:
        jumpo_list (list(dictionary)) : 스크래핑 한 점포 목록들
        category (str) : 업종명 예)편의점
        brand (str) : 브랜드명 예CU

    Returns:
        success (int) : DB에 성공적으로 저장한 점포의 개수
        fail (int) : DB에 저장 실패한 점포의 개수
        True (bool) : 저장 과정에서 오류가 발생했는지를 검증하는 불리언 값
    """
    category = Category.objects.get_or_create(category_name=category)[0]
    brand = Brand.objects.get_or_create(category=category, brand_name=brand)[0]
    success = fail = 0

    for jumpo in jumpo_list:
        try:
            Jumpo.objects.create(brand=brand, **jumpo)
            success += 1
        except django.db.utils.IntegrityError:
            print(f'>>> 이미 저장된 데이터({jumpo["jumpo_name"]})가 있습니다.')
            fail += 1
            pass

    return success, fail, True


def run():
    """
    서울특별시 전체 CU 편의점 목록을 스크래핑 하기 위해 선언한 모든 함수를 불러오는 함수
    """
    gu_list = get_district_info('서울특별시')
    gu_dong_dict = defaultdict(list)
    for gu in gu_list:
        gu_dong_dict[gu] = get_town_info(gu)

    jumpo_list = []

    for gu, dongs in gu_dong_dict.items():
        for dong in dongs:
            print(f'>>> {gu} {dong} 점포 데이터 스크래핑 성공')
            jumpo_list += get_jumpo_info(gu, dong)
            time.sleep(3)

    success, fail, result = save_data(jumpo_list)
    if result:
        print('>>> 성공적으로 데이터를 저장했습니다.')
        print(f'>>> 저장에 성공한 데이터 : {success}개\n 저장에 실패한 데이터 : {fail}개')


if __name__ == "__main__":
    run()
