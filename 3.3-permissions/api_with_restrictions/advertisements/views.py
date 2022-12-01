from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from advertisements.models import Advertisement
from advertisements.permissions import IsOwner
from advertisements.serializers import AdvertisementSerializer


class DateFilter(filters.FilterSet):
    date = filters.DateFromToRangeFilter()

    class Meta:
        model = Advertisement
        fields = ['created_at']


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = DateFilter
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create"]:
            return [IsAuthenticated()]
        if self.action in ["update", "partial_update"]:
            return [IsAuthenticated(), IsOwner()]
        if self.action in ["destroy"]:
            return [IsAuthenticated(), IsOwner()]
        return []
