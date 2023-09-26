from django.urls import path, include
from robots.views import ManagerReportView, ManagerReportCreateView
from robots.views import RobotsAddView

urlpatterns = [
    path('report/download/', ManagerReportCreateView.as_view(), name='download'),
    path('report/', ManagerReportView.as_view()),
    path('add/', RobotsAddView.as_view()),
]