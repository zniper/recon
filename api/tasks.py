from __future__ import absolute_import

from celery import Celery, shared_task
from recon.celery import app

from django.utils.log import getLogger


logger = getLogger(__name__)


@shared_task
def process_crawl_request(crawl_request):
    return crawl_request.source.crawl(True)
