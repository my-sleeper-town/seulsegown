'''store urls module'''
from django.urls import path
from store.views import index, result

urlpatterns = [
    path('', index, name='index'),
    path('result/', result, name='result'),
]
