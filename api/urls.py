from django.conf.urls import patterns, include, url

import views


urlpatterns = patterns('',
    url(r'^check/(?P<pk>\d+)/$', views.CheckResourceView.as_view(),
        name='check-resource'),
    url(r'^download/(?P<pk>\d+)/$', views.DownloadContentView.as_view(),
        name='download-content'),
    url(r'^clean/$', views.CleanContentView.as_view(),
        name='clean-content'),
    url(r'^requests/$', views.CrawlRequestListView.as_view(),
        name='request-list'),
    url(r'^requests/(?P<pk>\d+)/$', views.CrawlRequestDetailView.as_view(),
        name='request-detail'),
    url(r'^sources/$', views.SourceListView.as_view(),
        name='source-list'),
    url(r'^sources/(?P<pk>\d+)/$', views.SourceDetailView.as_view(),
        name='source-detail'),
    url(r'^schedules/$', views.CrawlScheduleListView.as_view(),
        name='schedule-list'),
    url(r'^schedules/(?P<pk>\d+)/$', views.CrawlScheduleDetailView.as_view(),
        name='schedule-detail'),
    url(r'^records/$', views.CrawlRecordListView.as_view(),
        name='record-list'),
    url(r'^records/(?P<pk>\d+)/$', views.CrawlRecordDetailView.as_view(),
        name='record-detail'),
)
