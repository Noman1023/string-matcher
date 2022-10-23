from django.conf import settings
from django.urls import path

from .views import *
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('', list_keys, name="keys"),
    path('matches', get_matches, name="matches")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
