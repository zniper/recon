from datetime import datetime

from django.db import models


class Resource(models.Model):
    """ This could be a single site or part of a site which contains wanted
        content
    """
    url = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    last_crawled = models.DateTimeField(default=datetime.now, blank=True)
    active = models.BooleanField(default=True)


class ItemRule(models.Model):
    resource = models.ForeignKey(Resource, related_name='rules')
    xpath = models.CharField(max_length=256)
    parent = models.ForeignKey('ItemRule', related_name='rules',
                               blank=True, null=True)


class Item(models.Model):
    """ Store single item information of links, images, text,...
    """
    url = models.CharField(max_length=256)
    resource = models.ForeignKey(Resource, related_name='items')
    hashed_value = models.CharField(max_length=256)
    added_time = models.DateTimeField(default=datetime.now)
    item_type = models.ForeignKey('ItemType', blank=True)
    local = models.ForeignKey('LocalItem', blank=True)
    children = models.ManyToManyField('Item', blank=True, null=True)


class ItemType(models.Model):
    name = models.CharField(max_length=256)


class LocalItem(models.Model):
    """ Specify local path of data item after being downloaded
    """
    created = models.DateTimeField(default=datetime.now)
    item_file = models.FileField(upload_to='items/%Y/%m/%d')
