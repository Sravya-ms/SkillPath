from django.urls import path
from . import views
urlpatterns = [
    path('exam/<int:topic_id>/', views.exam, name='exam'),
    path('planner/', views.planner, name='planner'),
    path('planner/<int:pk>/<str:action>/', views.session_action, name='session_action'),
]
