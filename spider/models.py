from datetime import datetime
from hashlib import sha1

from django.db import models

from  utils import Extractor


class Resource(models.Model):
    """ This could be a single site or part of a site which contains wanted
        content
    """
    url = models.CharField(max_length=256)
    name = models.CharField(max_length=256, blank=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return 'Resource: %s' % self.name


class ItemRule(models.Model):
    resource = models.ForeignKey(Resource, related_name='rules')
    xpath = models.CharField(max_length=256)
    parent = models.ForeignKey('ItemRule', related_name='rules',
                               blank=True, null=True)
    last_crawled = models.DateTimeField(blank=True, null=True)
    data_type = models.ForeignKey('DataType')

    def __unicode__(self):
        return 'Item Rule: %s' % self.xpath

    def crawl(self):
        """ Download content specified by this item rule
        """
        self.items.all().delete()

        attribs = self.data_type.fields.replace(' ', '') or ''
        attribs = [attr for attr in attribs.split(',') if attr]

        extractor = Extractor(self.resource.url)
        result, elements = extractor.extract(self.xpath, attribs)

        # download full content or extract data parts
        if self.data_type.is_body:
            for res in result:
                item = Item(rule=self)
                item.save()
                item.set_hashed_value()
                root = elements[result.index(res)]
                extractor.set_location(item.hashed_value)
                extractor.download_content(root=root)
                item.downloaded = True
                item.save()
        else:
            for res in result:
                item = Item(rule=self)
                item.save()
                for attr in attribs:
                    new_attr = ItemAttribute(item=item, key=attr,
                                             value=res.get(attr, ''))
                    new_attr.save()
                item.set_hashed_value()

        self.last_crawled = datetime.now()
        self.save()


class Item(models.Model):
    """ Store single item information of links, images, text,...
    """
    rule = models.ForeignKey('ItemRule', related_name='items')
    hashed_value = models.CharField(max_length=256, blank=True,
                                    default='', unique=True)
    children = models.ManyToManyField('Item', blank=True, null=True)
    downloaded = models.BooleanField(blank=True, default=False)

    def __unicode__(self):
        return 'Item of rule: %s' % str(self.rule)

    def set_hashed_value(self):
        if self.rule.data_type.is_body:
            raw = self.rule.resource.url + str(self.pk)
        else:
            keys = [key[0] for key in self.attributes.values_list('key')]
            values = [val[0] for val in self.attributes.values_list('value')]
            keys.sort()
            values.sort()
            raw = ''.join(keys + values)
        self.hashed_value = sha1(raw).hexdigest()
        self.save()


class ItemAttribute(models.Model):
    item = models.ForeignKey('Item', related_name='attributes')
    key = models.CharField(max_length=64)
    value = models.TextField()


class DataType(models.Model):
    name = models.CharField(max_length=64)
    fields = models.CharField(max_length=256, default='', blank=True)
    is_body = models.BooleanField(blank=True)

    def __unicode__(self):
        return 'Data type: %s' % str(self.name)

