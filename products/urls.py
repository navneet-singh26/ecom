from django.urls import path
from . import views

urlpatterns = [
    path('summary_report/', views.summary_report, name='summary_report'),
]
