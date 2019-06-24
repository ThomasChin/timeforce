from django.urls import path, include

from .views import ActivityList, ActivityDetail


urlpatterns = [
    path("api/activities", ActivityList.as_view()),
    path("api/activities/<uuid:pk>", ActivityDetail.as_view()),
]
