from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.contrib import admin

# add media url
from django.conf import settings
from django.conf.urls.static import static

# Django Rest Framework
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view
from api import views


app_name = 'server'

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('profiles', views.ProfileViewSet)
router.register('videos', views.VideoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/doc', get_swagger_view(title='Tape Viedo API')),
    path('main/video', include(router.urls)),
    path('', include(router.urls)),
    path('login', views.login),
    path('signup', views.signup),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
