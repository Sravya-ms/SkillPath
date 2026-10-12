from django.urls import path
from . import views
urlpatterns = [
    path('check/', views.check, name='job_check'),
    path('<int:pk>/', views.result, name='job_result'),
    path('<int:pk>/decide/', views.decide, name='job_decide'),
    path('<int:pk>/delete/', views.delete, name='job_delete'),
    path('task/<int:pk>/toggle/', views.toggle_task, name='task_toggle'),
]
