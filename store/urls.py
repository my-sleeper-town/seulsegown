from django.urls import path, include
from store.views import index, result


urlpatterns = [
    path('', index, name='index'),
    path('result/', result, name='result'),
]