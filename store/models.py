from django.db import models
from math import ceil
from utils.utils import get_latlng_range, get_distance

class Category(models.Model):
    category_name = models.CharField(max_length=50, verbose_name='업종명')

    def __str__(self):
        return self.category_name


class Brand(models.Model):
    brand_name = models.CharField(max_length=100, verbose_name='브랜드명')
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return self.brand_name


class Jumpo(models.Model):
    jumpo_name = models.CharField(max_length=50, verbose_name='점포명')
    street_address = models.CharField(max_length=200, verbose_name='도로명주소')
    latitude = models.FloatField(default=0, verbose_name='위도')
    longitude = models.FloatField(default=0, verbose_name='경도')
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.brand.brand_name} {self.jumpo_name}"

    def in_distance(latlng, distance):
        '''
        주어진 좌표에서 일정 거리 내의 점포를 어림잡아서 찾아서 반환합니다.

        Args:
            latlng (float, float): (lat, lng)로 표현된 위도경도쌍입니다.
            distance (float): 킬로미터 단위입니다.
        
        Returns:
            주어진 좌표로부터 일정 거리 내에 있는 jumpo의 리스트
        '''
        (min_latlng, max_latlng) = get_latlng_range(latlng, distance)
        jumpos = Jumpo.objects.filter(latitude__gte=min_latlng[0], latitude__lte=max_latlng[0], longitude__gte=min_latlng[1], longitude__lte=max_latlng[1])
        return jumpos

    
    def distance_to(self, latlng):
        """
        주어진 위도, 경도와 해당 점포의 거리를 계산하여 미터로 반환합니다.

        Args:
            latlng (float, float): (lat, lng)
        
        Returns:
            주어진 좌표와 해당 점포 사이의 거리입니다. 단위는 킬로미터입니다.
        """
        return get_distance(self.latitude, self.longitude, latlng[0], latlng[1])


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['jumpo_name', 'street_address'], name='jumpo_address'),
        ]
