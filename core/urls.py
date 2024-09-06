from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

app_name = 'core'

urlpatterns = [
    path("",index,name="home"),
    path("register/",register_view,name="register"),
    path("about_us/",about,name="about_us"),
    path("contact_us/",contact,name="contact_us"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
