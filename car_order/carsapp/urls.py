from django.urls import path, include
from rest_framework import routers
from .views import CarMakeViewSet, ColorViewSet, CarModelViewSet, OrderViewSet, OrderInfo

router = routers.DefaultRouter()
router.register(r'color', ColorViewSet)

router2 = routers.DefaultRouter()
router2.register(r'order', OrderViewSet)

router3 = routers.DefaultRouter()
router3.register(r'car_make', CarMakeViewSet)

router4 = routers.DefaultRouter()
router4.register(r'car_model', CarModelViewSet)


urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/', include(router2.urls)),
    path('api/v1/', include(router3.urls)),
    path('api/v1/', include(router4.urls)),
    path('order_info/', OrderInfo.as_view()),
    path('order_info/<int:sort>/', OrderInfo.as_view()),
    path('order_info/<str:sort>/', OrderInfo.as_view()),
]