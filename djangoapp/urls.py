from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from accounts import views as account_views
from search.views import search_view

from .views import home_view


urlpatterns = [
    path('', home_view),
    path('pictures/', include('media.urls')),
    path('search/', search_view, name='search'),
    path('admin/', admin.site.urls),
    path('accounts/login/', account_views.login_view),
    path('accounts/logout/', account_views.logout_view),
    path('accounts/register/', account_views.register_view),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
