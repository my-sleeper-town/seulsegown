from django.shortcuts import render
from django.http import Http404


def index(request):
    return render(request, 'store/index.html', {})


def result(request):
    if request.method == 'GET':
        address = request.GET.get('address', None)
        if address:
            if address.startswith('서울'):
                return render(request, 'store/result.html', {'address': address, })
            else:
                return Http404('현재는 서울특별시만 서비스를 제공하고 있습니다.')
        else:
            raise Http404("주소를 반드시 입력해주셔야 합니다.")


