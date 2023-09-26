from django.urls import path, include
from robots.views import RobotsAddView

urlpatterns = [
    path('add/', RobotsAddView.as_view()),
]
