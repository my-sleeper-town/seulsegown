from collections import defaultdict
from bs4 import BeautifulSoup
from utils.utils import addr_to_lat_lng
import django
import requests
import os
import time


"""
CU 편의점 목록과 주소를 가져오기 위한 함수들입니다.
CU 웹사이트는 시도명, 군구, 읍명동 등 특정 파라미터(DATA)로 POST 요청을 보내는 방식으로 동작하고 있습니다.
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
    while True:
        req = post_request(URLS['jumpo'], data=DATA, headers=HEADERS)
        soup = BeautifulSoup(req.text, 'html.parser')
        stores = soup.select(
            '#result_search > div.result_store > div.detail_store > table > tbody > tr')
        if stores[0].find('td').text == '등록된 게시물이 없습니다.':
            pass
        else:
            for store in stores:
                lat = 0
                lng = 0
                jumpo_name = store.find('span').text
                street_address = store.find('address').text.strip()
                latlng_address = addr_to_lat_lng(street_address)
                if latlng_address is not None:
                    try:
                        lng = latlng_address[0]
                        lat = latlng_address[1]
                    except IndexError as e:
                        print(f"Error occurred while extracting latitude and longitude from address {street_address}: {e}")
                        pass

                total_store_info.append({
                    'jumpo_name': jumpo_name,
                    'street_address': street_address,
                    'latitude': lat,
                    'longitude': lng,
                })

        if soup.select('#paging > a') and soup.select('#paging > a')[-1].text != '이전':
            DATA['pageIndex'] += 1
        else:
            break

    return total_store_info


def crawl_cu():
    """
    서울특별시 전체 CU 편의점 목록을 스크래핑 하기 위해 선언한 모든 함수를 불러오는 함수

    Returns:
        jumpos_info list(dictionary)-> [{'jumpo_name': '중랑베스트점',
                            'jumpo_street_address': '서울특별시 중랑구 봉화산로4길 28 (중화동)',
                            'latitude': 37.564214,
                            'longitude': 127.001699 }, ..{}.. , ]
    """
    gu_list = get_district_info('서울특별시')
    gu_dong_dict = defaultdict(list)
    for gu in gu_list:
        gu_dong_dict[gu] = get_town_info(gu)

    jumpos_info = []

    for gu, dongs in gu_dong_dict.items():
        for dong in dongs:
            jumpos_info += get_jumpo_info(gu, dong)
            time.sleep(1)

    return jumpos_info
