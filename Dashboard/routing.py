from django.urls import path

from .consumers import ChartConsumer

ws_urlpatterns = [
    path('ws/Graph/', ChartConsumer.as_asgi())
]