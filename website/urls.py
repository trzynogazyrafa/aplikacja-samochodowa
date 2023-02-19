from django.urls import path, include
from website.views import main_view, car_view
from rest_framework import routers
from website.views import UserViewSet, GroupViewSet, CarViewSet, CarList

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'cars', CarViewSet)

urlpatterns = [
    path("", main_view, name="main"),
    path("<int:pk>", car_view, name="car"),
    path(r'api/', include(router.urls)),
    # path(r"api/cars/(?P<power_min>,+)/%", CarList.as_view())
]