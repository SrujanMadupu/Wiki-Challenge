from django.urls import path
from .views import OpenSearch, WikiSearch, DownloadPDF

urlpatterns = [
    path('index/', OpenSearch.as_view()),
    path('search/', WikiSearch.as_view()),
    path('download/', DownloadPDF.as_view()),
]
