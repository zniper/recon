import json
import os

from zipfile import ZipFile

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.conf import settings

from rest_framework import generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response

from scraper.models import Source, LocalContent
from repository import models as repo_models

import serializers


class CheckResourceView(View):

    def get(self, *args, **kwargs):
        sid = kwargs.get('pk', None)
        content = LocalContent.objects.filter(source__pk=sid, state=0)
        content = content.order_by('created_time')
        content_list = []
        for item in content:
            content_list.append({
                'id': item.id,
                'original': item.url,
                'crawl_time': item.created_time.strftime('%Y-%m-%d %H:%M'),
            })
        return HttpResponse(json.dumps(content_list), mimetype='application/json')


class DownloadContentView(View):

    def get(self, *args, **kwargs):
        cid = kwargs.get('pk', None)
        content = LocalContent.objects.get(pk=cid)
        zip_path = self.zip_content(content)
        with open(zip_path, 'rb') as zfile:
            response = HttpResponse(
                zfile.read(), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="%s"' % \
                os.path.basename(zip_path)
        return response

    def zip_content(self, local_content):
        zip_path = local_content.local_path.rstrip('/') + '.zip'
        zfile = ZipFile(zip_path, 'w')
        for fn in os.listdir(local_content.local_path):
            fp = os.path.join(local_content.local_path, fn)
            zfile.write(fp, os.path.basename(fp))
        zfile.close()
        return zfile.filename


class CleanContentView(View):

    def get(self, *args, **kwargs):
        cids = self.request.GET.get('id').split(',')
        for content in LocalContent.objects.filter(pk__in=cids):
            content.remove_files()
        return HttpResponse('CLEANED: %s' % ', '.join(cids))


# CRAWL REQUESTS

class RequestListView(generics.ListCreateAPIView):
    queryset = repo_models.Request.objects.all()
    serializer_class = serializers.RequestSerializer


class RequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = repo_models.Request.objects
    serializer_class = serializers.RequestSerializer


# CRAWL SCHEDULE

class ScheduleListView(generics.ListCreateAPIView):
    queryset = repo_models.Schedule.objects.all()
    serializer_class = serializers.ScheduleSerializer


class ScheduleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = repo_models.Schedule.objects
    serializer_class = serializers.ScheduleSerializer


# CRAWL RECORDS

class RecordListView(generics.ListCreateAPIView):
    queryset = repo_models.Record.objects.all()
    serializer_class = serializers.RecordSerializer


class RecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = repo_models.Record.objects
    serializer_class = serializers.RecordSerializer
