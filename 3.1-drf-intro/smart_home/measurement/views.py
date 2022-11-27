# TODO: опишите необходимые обработчики, рекомендуется использовать generics APIView классы:
# TODO: ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView

from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .serializers import *


class Sensors(ListAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    def post(self, request):
        print(request)
        name = request.data.get('name', None)
        description = request.data.get('description', None)
        if name and description:
            Sensor(name=name, description=description).save()
            return Response({'Create': 'Success'})
        else:
            return Response({'Create': 'Failed'})


class OneSensor(APIView):

    def get_object(self, pk):
        return Sensor.objects.get(pk=pk)

    def get(self, request, pk):
        obj = self.get_object(pk)
        ser = SensorDetailSerializer(obj)
        return Response(ser.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        obj = self.get_object(pk)
        ser = SensorSerializer(obj, data=request.data, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        else:
            Response(ser.data, status=status.HTTP_400_BAD_REQUEST)


class Measurements(APIView):

    def get_object(self, pk):
        return Sensor.objects.get(pk=pk)

    def post(self, request):
        obj = self.get_object(request.data['sensor'])
        Measurement(sensor=obj, temperature=request.data['temperature']).save()
        return Response('Ok', status=status.HTTP_201_CREATED)
