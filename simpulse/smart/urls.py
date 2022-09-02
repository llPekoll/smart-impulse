from django.urls import path

from .views import InstallationList, CategoryList, DataList, GetPointCloud

urlpatterns = [
    path("installations", InstallationList.as_view()),
    path("categories", CategoryList.as_view()),
    path("data", DataList.as_view()),
    path("pc", GetPointCloud.as_view()),
]
