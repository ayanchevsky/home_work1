from django.urls import path
from measurement.views import *

urlpatterns = [
    # TODO: зарегистрируйте необходимые маршруты
    path('sensor/<pk>/', OneSensor.as_view()),
    path('sensor/', Sensors.as_view()),
    path('measurements/', Measurements.as_view()),

]
