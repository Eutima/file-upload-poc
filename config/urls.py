from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from core.views import FileUploadViewSet
from core.views import FileUploadView
from django.conf.urls.static import static
from django.conf import settings

router = DefaultRouter()
router.register(r'upload', FileUploadViewSet, basename='file-upload')

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += router.get_urls()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
