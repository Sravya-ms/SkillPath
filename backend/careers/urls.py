from django.urls import path
from . import views
urlpatterns = [
    path('', views.explore, name='explore'),
    path('goal/<slug:slug>/', views.set_goal, name='set_goal'),
    path('results/<int:pk>/', views.results, name='results'),
    path('career/<slug:slug>/', views.career_detail, name='career_detail'),
]
