import requests
import os
import shutil

from lxml import etree
from slugify import slugify
from urlparse import urljoin


EXCLUDED_ATTRIBS = ('html')


class Extractor(object):

    slug = ''

    def __init__(self, start_url, download_to=''):
        self.url = start_url
        self.page = self.parse_content()
        self.download_to = os.path.join(download_to or './', self.slug)

    def parse_content(self, url=''):
        url = url or self.url
        response = requests.get(url)
        self.slug = slugify(url.split('/')[-1])
        return etree.HTML(response.content)

    def extract(self, path, attribs=[]):
        """ Return dict of attributes of specified elements
                [{'attr0': 'value0', 'attr1': 'value1',...]
        """
        items = self.page.xpath(path)

        # exclude predefined attributes
        [attribs.remove(attr) for attr in EXCLUDED_ATTRIBS if attr in attribs]

        # If attributes are specified, dict will be returned instead
        response = []
        for item in items:
            item_dict = {}
            if 'text' in attribs:
                item_dict['text'] = item.text.strip() or ''
                attribs.remove('text')
            for attr in attribs:
                item_dict[attr] = item.get(attr, '')
            response.append(item_dict)
        return response, items

    def get_links(self, path):
        links = self.select(path)
        res = []
        for link in links:
            res.append({
                'url': link.get('href'),
                'text': link.text,
                })
        return res

    def get_images(self, root=None):
        """ Return list of images inside root_path under format:
                [{url1, src1}, {url2, src2},...]
        """
        root = root or self.page
        images = root.xpath('//img')
        res = []
        for img in images:
            res.append({
                'src': img.get('src'),
                'alt': img.get('alt')
                })
        return res

    def prepare_directory(self, clean=False):
        """ Create local directories if not existing 
        """
        try:
            os.makedirs(self.download_to)
        except OSError:
            pass

    def set_location(self, location=''):
        self.download_to = location

    def download_image(self, image_url, file_name=''):
        """ Download image from given url and will save with wanted file_name
            or auto-detected one
        """
        image_name = file_name or image_url.split('/')[-1].split('?')[0]
        try:
            image = requests.get(image_url)
        except requests.exceptions.MissingSchema:
            image_url = urljoin(self.url, image_url)
            image = requests.get(image_url)
        file_path = os.path.join(self.download_to, image_name)
        with open(file_path, 'wb') as imgfile:
            imgfile.write(image.content)
        return file_path

    def download_all_images(self, root=None):
        """ Find and download all images inside the root_path
        """
        root = root or self.page
        images = self.get_images(root)
        file_list = []
        for img in images:
            file_list.append(self.download_image(img['src']))
        return file_list

    def download_content(self, root=None, with_image=True):
        """ Download the whole content and images and save to local
        """
        root = root or self.page
        self.prepare_directory(True)
        content = etree.tostring(root, pretty_print=True)
        with open(os.path.join(self.download_to, 'index.html'), 'wb') as hfile:
            hfile.write(content)
        if with_image:
            self.download_all_images(root)
        return self.download_to
