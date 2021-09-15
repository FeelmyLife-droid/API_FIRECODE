from django.urls import path

from rest_framework import routers

from apiback.views import CityListCreate, ShopListCreate

router = routers.SimpleRouter()
router.register(r'city', CityListCreate)
router.register(r'shop', ShopListCreate)

urlpatterns = [

]
urlpatterns += router.urls
