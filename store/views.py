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
    if address or lnglat is None:
        if address.startswith('서울'):
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
        else:
            return render(request, 'store/error.html', {})
    else:
        return render(request, 'store/error2.html', {})


