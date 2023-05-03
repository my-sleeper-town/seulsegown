# 위도 경도
import requests
from urllib.parse import urlparse
import json
import os

token = os.getenv('KAKAO_TOKEN')


def addr_to_lat_lng(addr):
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query={address}'.format(address=addr)
    headers = {"Authorization": "KakaoAK " + token}
    
    try:
        response = requests.get(url, headers=headers)
        result = json.loads(response.text)
        match_first = result['documents'][0]['address']
        return float(match_first['x']), float(match_first['y'])
    
    except (requests.exceptions.RequestException, ValueError, KeyError, IndexError) as e:
        print(f"Error occurred: {e}")
        pass 

