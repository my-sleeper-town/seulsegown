import os
import requests

token = os.getenv('KAKAO_API_TOKEN')

BASE_URL = 'https://dapi.kakao.com/v2/'

if not token:
    print("KAKAO_API_TOKEN is not set")
    exit

def _call_api(url):
    headers = {'Authorization': f'KakaoAK {token}'}
    response = requests.get(BASE_URL + url, headers=headers)
    return response.json()

def get_latlng(address):
    """
    address: 주소
    returns: (lat, lng) (or None when not found)
    """
    response = _call_api('local/search/address.json?query={}'.format(address))
    try:
        return response['documents'][0]['y'], response['documents'][0]['x']
    except:
        return None
