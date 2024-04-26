from django.contrib import admin
from django.urls import path
from resume_extractor_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.upload_zip, name='upload_zip'),
]
