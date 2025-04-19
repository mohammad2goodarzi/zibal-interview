from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.TransactionListAPIView.as_view()),
]
