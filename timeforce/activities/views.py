from rest_framework import generics

from .models import Activity
from .serializers import ActivitySerializer


class ActivityList(generics.ListCreateAPIView):
    serializer_class = ActivitySerializer

    def get_queryset(self):
        user = self.request.user.id
        return Activity.objects.filter(owner=user)


class ActivityDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ActivitySerializer

    def get_queryset(self):
        user = self.request.user.id
        return Activity.objects.filter(owner=user)
