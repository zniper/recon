from django.conf.urls import patterns, url

import views


urlpatterns = patterns('',
    url(r'^requests/$', views.RequestListView.as_view(),
        name='request-list'),
    url(r'^requests/(?P<pk>\d+)/$', views.RequestDetailView.as_view(),
        name='request-detail'),
    url(r'^schedules/$', views.ScheduleListView.as_view(),
        name='schedule-list'),
    url(r'^schedules/(?P<pk>\d+)/$', views.ScheduleDetailView.as_view(),
        name='schedule-detail'),
    url(r'^records/$', views.RecordListView.as_view(),
        name='record-list'),
    url(r'^records/(?P<pk>\d+)/$', views.RecordDetailView.as_view(),
        name='record-detail'),

    url(r'^check/(?P<pk>\d+)/$', views.CheckResourceView.as_view(),
        name='check-resource'),
    url(r'^download/(?P<pk>\d+)/$', views.DownloadContentView.as_view(),
        name='download-content'),
    url(r'^clean/$', views.CleanContentView.as_view(),
        name='clean-content'),
)
