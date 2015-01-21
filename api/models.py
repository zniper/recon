from django.db import models


class CrawlRequest(models.Model):
    source = models.ForeignKey('scraper.Source')
    schedule = models.ForeignKey('CrawlSchedule')
    # UID of processing task
    task = models.CharField(max_length=128, blank=True, null=True)


class CrawlSchedule(models.Model):
    """ Defines the schedule for a specific crawl action """

    effective = models.DateTimeField(help_text="Starting time")
    repeat = models.IntegerField(blank=True, null=True,
                                 help_text="Recrawl after given minutes")
    expire = models.DateTimeField(blank=True, null=True,
                                  help_text="Expiring time")


class CrawlRecord(models.Model):
    request = models.ForeignKey('CrawlRequest', related_name='records')
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=64)
    result = models.ForeignKey('scraper.LocalContent')
