import os

from datetime import datetime

from django.db import models
from django.conf import settings

from utils import Extractor


class Resource(models.Model):
    """ This could be a single site or part of a site which contains wanted
        content
    """
    url = models.CharField(max_length=256)
    name = models.CharField(max_length=256, blank=True, null=True)
    active = models.BooleanField(default=True)
    link_xpath = models.CharField(max_length=255)
    expand_rules = models.TextField(blank=True, null=True)
    crawl_depth = models.PositiveIntegerField(default=1)
    content_xpath = models.CharField(max_length=255)
    meta_xpath = models.TextField(default='', blank=True)
    refine_rules = models.TextField(default='', blank=True)
    black_words = models.ForeignKey('WordSet', blank=True, null=True)

    def __unicode__(self):
        return 'Resource: %s' % self.name

    def crawl(self, download=True):
        # Custom definitions
        metapath = eval(self.meta_xpath)
        rules = [item.strip() for item in self.refine_rules.split('\n')
                 if item.strip()]

        extractor = Extractor(self.url, settings.CRAWL_ROOT)
        all_links = extractor.extract_links(
            xpath=self.link_xpath,
            expand_rules=self.expand_rules.split('\n'),
            depth=self.crawl_depth)

        if download:
            # Get the black words
            blacklist = self.black_words.words.split('\n')

            for link in all_links:
                link_url = link['url']
                if LocalContent.objects.filter(url=link_url).count():
                    print 'Bypass %s' % link_url
                    continue
                print 'Download %s' % link_url
                location = datetime.now().strftime('%Y/%m/%d')
                location = os.path.join(settings.CRAWL_ROOT, location)
                sub_extr = Extractor(link_url, location)
                local_path = sub_extr.extract_content(self.content_xpath,
                                                      metapath=metapath,
                                                      custom_rules=rules,
                                                      blacklist=blacklist)
                content = LocalContent(url=link_url, resource=self,
                                       local_path=local_path)
                content.save()


class LocalContent(models.Model):
    url = models.CharField(max_length=256)
    resource = models.ForeignKey('Resource', related_name='content')
    local_path = models.CharField(max_length=256)
    created_time = models.DateTimeField(default=datetime.now,
                                        blank=True, null=True)

    def __unicode__(self):
        return 'Local Content: %s' % self.url


class WordSet(models.Model):
    """ Class words in to set for filtering purposes """
    name = models.CharField(max_length=64)
    words = models.TextField()

    def save(self, *args, **kwargs):
        """ Normalize all words in set """
        good_list = []
        for word in self.words.lower().split('\n'):
            word = word.strip()
            if word and word not in good_list:
                good_list.append(word)
        self.words = '\n'.join(good_list)
        return super(WordSet, self).save(*args, **kwargs)

    def __unicode__(self):
        return 'Words: %s' % self.name
