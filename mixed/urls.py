from django.conf.urls import patterns, url

urlpatterns = patterns(
    'mixed.apis',
    url(r'^api/$', 'document_list'),
    url(r'^api/(?P<slug>.*)/$', 'document'),
)

urlpatterns += patterns(
    'mixed.views',
    url(r'^a/create/$', 'document_create', name='create'),
    url(r'^a/edit/(?P<slug>.*)/$', 'document_edit', name='edit'),
    # url(r'^a/save/$', 'document_save', name='save'),
    url(r'^a/delete/(?P<slug>.*)/$', 'document_delete', name='delete'),
    url(r'^$', 'document_list', name='list'),
    url(r'^(?P<slug>.*)/$', 'document_view', name='view'),
)