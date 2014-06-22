import requests
import os

from lxml import etree
from slugify import slugify
from urlparse import urljoin


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

    def select(self, path):
        return self.page.xpath(path)

    def get_links(self, path):
        links = self.select(path)
        res = []
        for link in links:
            res.append({
                'url': link.get('href'),
                'text': link.text,
                })
        return res

    def get_images(self, root_path=''):
        """ Return list of images inside root_path under format:
                [{url1, src1}, {url2, src2},...]
        """
        root_path = root_path or '//'
        root = self.page.xpath(root_path)[0]
        images = root.xpath('//img')
        res = []
        for img in images:
            res.append({
                'src': img.get('src'),
                'alt': img.get('alt')
                })
        return res

    def prepare_directory(self):
        """ Create local directories if not existing 
        """
        if not os.path.exists(self.download_to):
            os.makedirs(self.download_to)

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
        self.prepare_directory()
        file_path = os.path.join(self.download_to, image_name)
        with open(file_path, 'wb') as imgfile:
            imgfile.write(image.content)
        return file_path

    def download_all_images(self, root_path=''):
        """ Find and download all images inside the root_path
        """
        root_path = root_path or '//'
        images = self.get_images(root_path)
        file_list = []
        for img in images:
            file_list.append(self.download_image(img['src']))
        return file_list

    def download_content(self, root_path='', with_image=True):
        """ Download the whole content and images and save to local
        """
        root_path = root_path or '//'
        root = self.page.xpath(root_path)[0]
        self.prepare_directory()
        content = etree.tostring(root, pretty_print=True)
        with open(os.path.join(self.download_to, 'index.html'), 'wb') as hfile:
            hfile.write(content)
        if with_image:
            self.download_all_images(root_path)
        return self.download_to
