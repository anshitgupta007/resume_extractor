from django.contrib import admin
from django.urls import path
from resume_extractor_app import views
from  django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.upload_zip, name='upload_zip'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
