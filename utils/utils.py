"""Utils module

This module provide functions to calculate distance, get latlng range, etc.
"""

import math
import requests
import json
import os

# 터미널에서 export로 키를 저장하시면 됩니다.
token = os.getenv('KAKAO_TOKEN')

EARTH_RADIUS = 6371  # 지구 반지름(km)

def calculate_seulsegown_score(jumpos):
    '''
    dict로 구성된 리스트를 받아 슬세권 점수를 계산합니다.

    세부적인 계산 방법은 아래와 같습니다:

        - 리스트의 편의시설을 아래의 방법대로 점수를 매겨서 합산합니다.
            - 200m 내에 있는 편의시설은 3점
            - 300m 내에 있는 편의시설은 2점
            - 400m 내에 있는 편의시설은 1점
        - 만점은 10점으로 10점을 넘기지 않습니다.

    Args:
        jumpos (dict): {distance: 현재 위치와의 거리(m단위)}

    Returns:
        int: 0 이상 10 이하의 점수
    '''

    score = 0
    for jumpo in jumpos:
        if jumpo['distance'] <= 200:
            score += 3
        elif jumpo['distance'] <= 300:
            score += 2
        elif jumpo['distance'] <= 400:
            score += 1
    score = score if score < 10 else 10
    return score

def get_latlng_range(latlng, distance):
    """
    주어진 위도, 경도를 기준으로 특정 거리만큼 떨어져있는 반경을 반환합니다.

    Args:
        latlng (tuple): (lat, lng)
        distance (float): kilometer
    
    Returns:
        a tuple represents (min_latlng, max_latlng)
    """
    lat, lng = latlng

    lat_degree_dist = EARTH_RADIUS * math.pi / 180
    lon_degree_dist = EARTH_RADIUS * math.pi * math.cos(lat * math.pi / 180) / 180

    lat_diff = distance / lat_degree_dist
    lng_diff = distance / lon_degree_dist

    return (
        (lat - lat_diff, lng - lng_diff), # min
        (lat + lat_diff, lng + lng_diff), # max
    )


def get_distance(lat1, lng1, lat2, lng2):
    """
    Calculate the distance between two points on the Earth's surface using the Haversine formula.

    Args:
        lat1 (float): The latitude of the first point.
        lng1 (float): The longitude of the first point.
        lat2 (float): The latitude of the second point.
        lng2 (float): The longitude of the second point.

    Returns:
        The distance (in kilometers) between the two points.
    """
    d_lat = math.radians(lat2 - lat1)
    d_lng = math.radians(lng2 - lng1)
    a = math.sin(d_lat/2) * math.sin(d_lat/2) + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
        math.sin(d_lng/2) * math.sin(d_lng/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = EARTH_RADIUS * c
    return distance


# 주소를 받아 위도 경도로 변환하기
def addr_to_lat_lng(addr):
    url = f'https://dapi.kakao.com/v2/local/search/address.json?query={addr}'
    headers = {'Authorization': 'KakaoAK ' + token} # token에 kakao api 키를 저장하시면 됩니다

    try:
        response = requests.get(url, headers=headers, timeout=5)
        result = json.loads(response.text)
        match_first = result['documents'][0]['address']
        return float(match_first['x']), float(match_first['y'])

    except (requests.exceptions.RequestException, TypeError, ValueError, KeyError, IndexError) as e:
        print(f'Error occurred: {e} while fetching address: {addr}')
