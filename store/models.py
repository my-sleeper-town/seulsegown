from django.db import models


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
        return f"{self.jumpo_name} - {self.street_address}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['jumpo_name', 'street_address'], name='jumpo_address'),
        ]
