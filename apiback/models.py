from django.core.exceptions import BadRequest

from django.db import models


class City(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название', unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class Street(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    city_title = models.ForeignKey('City', on_delete=models.CASCADE, related_name='street')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Улица'
        verbose_name_plural = 'Улицы'
        constraints = [
            models.UniqueConstraint(fields=['title', 'city_title'], name='unique_street')
        ]


class Shop(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    city = models.ForeignKey('City', on_delete=models.CASCADE, related_name='shop_in_city')
    street = models.ForeignKey('Street', on_delete=models.CASCADE, related_name='street_in_city')
    house = models.PositiveSmallIntegerField()
    time_open = models.TimeField()
    time_close = models.TimeField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        queryset = Street.objects.select_related('city_title').filter(city_title_id=self.city_id)
        if self.street_id in [street.pk for street in queryset]:
            super().save(*args, **kwargs)
        else:
            raise BadRequest(f'У {self.city} нет такой улицы {self.street}')

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'
        constraints = [
            models.UniqueConstraint(fields=['title', 'city', 'street', 'house'], name='unique_shop')
        ]
