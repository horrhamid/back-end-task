from django.urls import path, include
from rest_framework import routers
from .views import AppsView, AppView, AppRunView

urlpatterns = [
    path('apps/', AppsView.as_view()),
    path('apps/<int:app_id>/', AppView.as_view()),
    path('apps/<int:app_id>/run/', AppRunView.as_view()),
]
