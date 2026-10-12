from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('students.urls')),
    path('resumes/', include('resumes.urls')),
    path('careers/', include('careers.urls')),
    path('learning/', include('learning.urls')),
    path('jobs/', include('jobs.urls')),
]
