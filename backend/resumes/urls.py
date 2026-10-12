from django.urls import path
from . import views
urlpatterns = [
    path('upload/', views.upload, name='upload'),
    path('<int:pk>/review/', views.review, name='review'),
    path('<int:pk>/delete/', views.delete, name='resume_delete'),
]
