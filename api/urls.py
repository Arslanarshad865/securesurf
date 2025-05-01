from django.urls import path
from .views import URLAnalyzerView

urlpatterns = [
    path('analyze/', URLAnalyzerView.as_view(), name='analyze_url'),
]