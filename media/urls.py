from django.urls import path
from .views import (
    media_list_view,
    media_create_view,
    media_detail_view,
)

app_name = 'media'

urlpatterns = [
    path('', media_list_view, name='list'),
    path('create/', media_create_view, name='create'),
    path('<int:id>/', media_detail_view, name='detail'),
]
