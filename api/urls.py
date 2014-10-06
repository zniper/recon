from django.conf.urls import patterns, include, url

from views import CheckResourceView, DownloadContentView, CleanContentView

urlpatterns = patterns('',
    url(r'^check/(?P<pk>\d+)/$', CheckResourceView.as_view(),
        name='check-resource'),
    url(r'^download/(?P<pk>\d+)/$', DownloadContentView.as_view(),
        name='download-content'),
    url(r'^clean/$', CleanContentView.as_view(),
        name='clean-content'),
)
