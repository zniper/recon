import requests
import os

from lxml import etree
from urlparse import urljoin
from hashlib import sha1


EXCLUDED_ATTRIBS = ('html')


class Extractor(object):
    url = ''
    hash_value = ''

    def __init__(self, url, base_dir=''):
        self.url = url
        self.base_dir = base_dir
        self.hash_value, self.root = self.parse_content(url)
        self.set_location(self.hash_value)

    def parse_content(self, url=''):
        """ Return hashed value and etree object of target page 
        """
        response = requests.get(url)
        hash_value = sha1(url).hexdigest()
        return hash_value, etree.HTML(response.content)

    def set_location(self, location=''):
        self.download_to = os.path.join(self.base_dir, location)

    def extract_links(self, xpath, expand_rules=None, depth=1):
        all_links = []

        # First, crawl all links in the current page
        elements = self.root.xpath(xpath)
        for el in elements:
            all_links.append({
                'url': self.complete_url(el.get('href')),
                'text': el.text,
                })

        # Check if going to next page
        if depth > 1:
            for rule in expand_rules:
                for path in self.root.xpath(rule):
                    url = self.complete_url(path)
                    sub_extractor = Extractor(url)
                    sub_links = sub_extractor.extract_links(
                        xpath, expand_rules, depth-1)
                    all_links.extend(sub_links)

        return all_links

    def complete_url(self, path):
        if path.strip().lower()[:7] != 'http://':
            path = urljoin(self.url, path)
        return path

    def extract_content(self, xpath, with_image=True):
        """ Download the whole content and images and save to local
        """
        node = self.root.xpath(xpath)[0]

        # Create dir and download HTML content
        self.prepare_directory()
        content = etree.tostring(node, pretty_print=True)

        # Download images if required
        if with_image:
            image_paths = node.xpath('//img/@src')
            for ipath in image_paths:
                file_name = self.download_image(ipath)
                content = content.replace(ipath, file_name)

        # Finally, write to HTML file
        with open(os.path.join(self.download_to, 'index.html'), 'wb') as hfile:
            hfile.write(content)

        return self.download_to

    def prepare_directory(self):
        """ Create local directories if not existing 
        """
        try:
            os.makedirs(self.download_to)
        except OSError:
            pass

    def download_image(self, image_url):
        """ Download image from given url and save to common location 
        """
        image_name = image_url.split('/')[-1].split('?')[0]
        try:
            image = requests.get(image_url)
        except requests.exceptions.MissingSchema:
            image_url = urljoin(self.url, image_url)
            image = requests.get(image_url)
        file_path = os.path.join(self.download_to, image_name)
        with open(file_path, 'wb') as imgfile:
            imgfile.write(image.content)
        return image_name
