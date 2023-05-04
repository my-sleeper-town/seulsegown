# 거리 계산
import math


# 위도 경도
import requests
from urllib.parse import urlparse
import json
import os

# 터미널에서 export로 키를 저장하시면 됩니다. 
token = os.getenv('KAKAO_TOKEN')


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
    earth_radius = 6371  # 지구 반지름(km)
    d_lat = math.radians(lat2 - lat1)
    d_lng = math.radians(lng2 - lng1)
    a = math.sin(d_lat/2) * math.sin(d_lat/2) + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
        math.sin(d_lng/2) * math.sin(d_lng/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = earth_radius * c
    return distance


# 주소를 받아 위도 경도로 변환하기
def addr_to_lat_lng(addr):
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query={address}'.format(address=addr)
    headers = {"Authorization": "KakaoAK " + token} # token에 kakao api 키를 저장하시면 됩니다. 
    
    try:
        response = requests.get(url, headers=headers)
        result = json.loads(response.text)
        match_first = result['documents'][0]['address']
        return float(match_first['x']), float(match_first['y'])
    
    except (requests.exceptions.RequestException, TypeError, ValueError, KeyError, IndexError) as e:
        print(f"Error occurred: {e} while fetching address: {addr}")
        pass 