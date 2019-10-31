"""data URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mbtb import views

from django.http import HttpResponse


def empty_view(request):
    return HttpResponse("Empty View")


urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'AutopsyType', views.AutopsyTypeAPIView.as_view(), name="autopsy-type"),
    path(r'BrainDataset', views.BrainDatasetAPIView.as_view(), name="brain-dataset"),
    path(r'DatasetOthrDetails', views.DatasetOthrDetailsAPIView.as_view(), name="dataset-other-details"),
    path(r'ImageRepository', views.ImageRepositoryAPIView.as_view(), name="image-repository"),
    path(r'NeurodegenerativeDiseases', views.NeurodegenerativeDiseasesAPIView.as_view(),
         name="neurodegenerative-diseases"),
    path(r'TissueType', views.TissueTypeAPIView.as_view(), name="tissue-type"),
    path('', empty_view, name='empty_view'),

]
