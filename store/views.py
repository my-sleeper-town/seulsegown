from django.shortcuts import render
from django.http import Http404
from store.models import Jumpo
from utils.utils import addr_to_lat_lng
import math

def index(request):
    return render(request, 'store/index.html', {})

def result(request):
    address = request.GET.get('address', None)

    # 사용자가 입력한 주소의 위도, 경도 쌍
    lnglat = addr_to_lat_lng(address)
    print(lnglat)
    print(address)
    
    # 지역
    area = [
        '경기도', '강원도', '충청북도','충청남도', '전라북도', 
        '전라남도','경상북도','경상남도', '제주도', '부산광역시', 
        '대구광역시', '인천광역시', '광주광역시', '대전광역시', 
        '울산광역시', '세종시' '대구','부산', '인천', 
        '광주', '대전', "울산", "세종", '경기', '충남',
        '전북', '전남', '경북', '경남', "제주"
    ]
    seoul_region = [
        "종로구", "중구", "용산구", "성동구", "광진구", 
        "동대문구", "중랑구", "성북구", "강북구", "도봉구", 
        "노원구", "은평구", "서대문구", "마포구", "양천구", 
        "강서구", "구로구", "금천구", "영등포구", "동작구",
        "관악구", "서초구", "강남구", "송파구", "강동구"
    ]

    # case 1: 서울인 경우
    if address.startswith('서울') or address.split(' ')[0] in seoul_region:
        (lng, lat) = lnglat

        # 사용자의 위치로부터 0.5km 정도 떨어진 점포 목록
        jumpos = Jumpo.in_distance((lat, lng), 0.5)

        # 점포 딕셔너리 리스트
        jumpos = [
            {
                # 점포 이름
                'jumpo_name': jumpo.__str__(),

                # 사용자와 떨어진 거리 (미터 단위)
                'distance': math.floor(jumpo.distance_to((lat, lng)) * 1000),

                # 위치 (위도, 경도)
                'position': (jumpo.latitude, jumpo.longitude),

                # 브랜드 이름
                'brand': jumpo.brand.brand_name,
            } for jumpo in jumpos
        ]

        # address: 사용자가 입력한 주소
        # position: 위도, 경도 쌍
        # jumpos: 사용자 근처의 점포 목록
        return render(request, 'store/result.html', {'address': address, 'position': (lat, lng), 'jumpos': sorted(jumpos, key=lambda x: x['distance'])})
    # 서울이 아닌경우
    else:
        # 입력이 빈칸인 경우
        if address == '':
            return render(request, 'store/error_input_empty.html', {})
        # 다른 지역인 경우
        elif address.split(' ')[0] in area:
            return render(request, 'store/error_no_service_area.html', {})
        # 잘못 입력했을 경우
        else:
            return render(request, 'store/error_invalid_address.html', {})


