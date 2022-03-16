from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.contrib.auth import views as auth_views
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
    path("accounts/password_reset/",
         account_views.password_reset_view, name="password_reset"),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password/password_reset_done.html'), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="accounts/password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password/password_reset_complete.html'), name='password_reset_complete'),
    # path('accounts/', include('django.contrib.auth.urls')),
    # re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #         account_views.activate, name='activate'),
    path('activate/<uidb64>/<token>', account_views.activate, name='activate'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
