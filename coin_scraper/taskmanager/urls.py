from django.urls import path
from .views import StartScrapingView, ScrapingStatusView

urlpatterns = [
    path('start_scraping/', StartScrapingView.as_view(), name='start_scraping'),
    path('scraping_status/<str:job_id>/', ScrapingStatusView.as_view(), name='scraping_status'),
]
