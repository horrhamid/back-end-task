from django.urls import path, include
from rest_framework import routers
from .views import AppsView, AppView, AppRunView, AppHistoryView

urlpatterns = [
    path('apps/', AppsView.as_view()),
    path('apps/<int:app_id>/', AppView.as_view()),
    path('apps/<int:app_id>/run/', AppRunView.as_view()),
    path('apps/<int:app_id>/history/', AppHistoryView.as_view()),
]
