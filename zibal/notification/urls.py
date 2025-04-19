from django.urls import path
from . import views

urlpatterns = [
    path('send/', views.SendNotificationAPIView.as_view()),
]
