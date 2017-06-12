from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.contrib.auth.views import login, logout_then_login

from mixed.forms import AuthenticationForm
from mixed import views as mixed_view
from tblwork import views as tblwork


urlpatterns = [
    url(r'^table/paging/(?P<table_name>[^/]*)/(?P<page_size>[1-9]\d*)/(?P<page_id>[1-9]\d*)/$', tblwork.page),
    url(r'^table/paging/(?P<table_name>[^/]*)/(?P<page_size>[1-9]\d*)/$', tblwork.page),
    url(r'^table/paging/(?P<table_name>[^/]*)/$', tblwork.page),
    url(r'^table/test/(?P<table_name>[^/]*)/$', tblwork.test_set),
    url(r'^$', RedirectView.as_view(url="/document")),
    url(r'^document/', include('mixed.urls')),
    url(r'^accounts/profile/$', RedirectView.as_view(url="/document")),
    url(r'^accounts/login/$', login, {'authentication_form': AuthenticationForm}, name='login'),
    url(r'^accounts/logout/$', logout_then_login, name='logout'),
    url(r'^accounts/register/$', mixed_view.register, name='signin'),
    url(r'^super/', admin.site.urls),
]

urlpatterns += [
    url(r'^manmail/set/$', mixed_view.set_manmail_account),
    url(r'^manmail/send/(?P<m_type>[a-z]{3,10})/(?P<period>[\d|.]*)/$', mixed_view.send_manmail),
    url(r'^manmail/send/$', mixed_view.send_manmail, name='manmail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

try:
    from rismo import views as rismo
    urlpatterns += url(r'^rismo/taxmarks/taxapproach/', rismo.taxapproach),
    urlpatterns += url(r'^rismo/trade/', rismo.trade),
    urlpatterns += url(r'^rismo/user/', rismo.user_info),
except:
    pass
