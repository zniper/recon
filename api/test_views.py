import json

from datetime import datetime, timedelta

from django.test import TestCase
from django.core.urlresolvers import reverse


class SourceListViewTestCase(TestCase):
    fixtures = ['fixtures/sources.json']
    url = reverse('source-list')

    def test_index(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 200)

    def test_create_source(self):
        data = {
            "name": "TinhTe",
            "url": "https://www.tinhte.vn/forums/ios-tin-tuc-danh-gia.118/",
            "refine_rules": "",
            "expand_rules": "",
            "extra_xpath": "",
            "crawl_depth": 1,
            "meta_xpath": "{\"title\": \"//h1/text()\"}",
            "link_xpath": "/+//h3[@class=\"title\"]/a",
            "content_xpath": "//article",
            "active": True,
            "download_image": True,
        }
        res = self.client.post(self.url, data)
        self.assertEquals(res.status_code, 201)
        source = json.loads(res.content)
        self.assertGreater(source['id'], 0)


class SourceDetailView(TestCase):
    fixtures = ['fixtures/sources.json']
    url = reverse('source-detail', kwargs={'pk': 3})

    def test_view(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 200)
        source = json.loads(res.content)
        self.assertGreater(source['id'], 0)

    def test_update(self):
        data = {
            "name": "TinhTe Updated",
            "url": "http://google.com",
            "refine_rules": "rule 0",
            "expand_rules": "rule 1",
            "extra_xpath": "xpath 0",
            "crawl_depth": 2,
            "meta_xpath": "xpath 2",
            "link_xpath": "xpath 3",
            "content_xpath": "xpath 4",
            "active": False,
            "download_image": False,
        }
        res = self.client.put(self.url, data=json.dumps(data),
                              content_type='application/json')
        self.assertEqual(res.status_code, 200)
        source = json.loads(res.content)
        self.assertEqual(source['id'], 3)
        for item in data.keys():
            self.assertEqual(data[item], source[item])

    def test_delete(self):
        res = self.client.delete(self.url)
        self.assertEqual(res.status_code, 204)
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 404)


class CrawlRequestListViewTestCase(TestCase):
    fixtures = ['fixtures/sources.json',
                'fixtures/crawl_schedules.json',
                'fixtures/crawl_requests.json']
    url = reverse('request-list')

    def test_index(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 200)

    def test_create_request(self):
        data = {
            'source': 3,
            'schedule': 1,
        }
        res = self.client.post(self.url, data)
        self.assertEquals(res.status_code, 201)
        request = json.loads(res.content)
        self.assertGreater(request['id'], 0)


class CrawlRequestDetailView(TestCase):
    fixtures = ['fixtures/sources.json',
                'fixtures/crawl_schedules.json',
                'fixtures/crawl_requests.json']
    url = reverse('request-detail', kwargs={'pk': 1})

    def test_view(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 200)
        request = json.loads(res.content)
        self.assertGreater(request['id'], 0)

    def test_update(self):
        data = {
            "source": 5,
            "task": "HELLO TASK!",
            "schedule": 1
        }
        res = self.client.put(self.url, data=json.dumps(data),
                              content_type='application/json')
        self.assertEqual(res.status_code, 200)
        request = json.loads(res.content)
        self.assertEqual(request['id'], 1)
        for item in data.keys():
            self.assertEqual(data[item], request[item])

    def test_delete(self):
        res = self.client.delete(self.url)
        self.assertEqual(res.status_code, 204)
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 404)


class CrawlScheduleListViewTestCase(TestCase):
    fixtures = ['fixtures/sources.json',
                'fixtures/crawl_schedules.json']
    url = reverse('schedule-list')

    def test_index(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 200)

    def test_create_request(self):
        data = {
            'effective': datetime.now(),
            'repeat': 1,
            'expire': datetime.now()+timedelta(2)
        }
        res = self.client.post(self.url, data)
        self.assertEquals(res.status_code, 201)
        schedule = json.loads(res.content)
        self.assertGreater(schedule['id'], 0)
