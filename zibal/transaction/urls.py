from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.TransactionListAPIView.as_view()),
    path('list/v2/', views.TransactionListV2APIView.as_view()),
]
