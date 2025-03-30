from django.urls import path
from .views import DashboardData

urlpatterns = [
    path('api/dashboard/', DashboardData.as_view(), name='dashboard_data'),
]
