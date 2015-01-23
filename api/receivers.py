from django.dispatch import receiver
from django.db import models

from .models import CrawlRequest
from .tasks import process_crawl_request


@receiver(models.signals.post_save, sender=CrawlRequest)
def handle_crawl_request(sender, instance, *args, **kwargs):
    process_crawl_request.delay(instance)
