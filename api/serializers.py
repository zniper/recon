from rest_framework import serializers
from scraper.models import Source

from repository import models as repo_models


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = repo_models.Request


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = repo_models.Schedule


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = repo_models.Record

"""
class CombinedCrawlRequestSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    task = serializers.CharField(required=False, allow_blank=True,
                                 max_length=128)
    # Schedule fields
    effective = serializers.DateTimeField(required=False)
    expire = serializers.DateTimeField(required=False)
    repeat = serializers.IntegerField(required=False)
    # Source fields
    url = serializers.CharField(max_length=512)
    link_xpath = serializers.CharField(max_length=512)
    expand_rules = serializers.CharField(allow_blank=True)
    crawl_depth = serializers.IntegerField(default=1)
    content_xpath = serializers.CharField(max_length=256)
    meta_xpath = serializers.CharField(allow_blank=True)
    refine_rules = serializers.CharField(allow_blank=True)
    download_image = serializers.BooleanField(default=True)


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source


class CrawlRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrawlRecord

"""
