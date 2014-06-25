from django.core.management.base import NoArgsCommand

from spider.models import Resource


class Command(NoArgsCommand):
    """ Crawl all active resources """

    def handle_noargs(self, **options):
        resources = Resource.objects.filter(active=True)
        for res in resources:
            print 'Crawling %s' % res.name
            res.crawl()
