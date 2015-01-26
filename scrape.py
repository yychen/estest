#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from lxml import etree
from pyelasticsearch import ElasticSearch

from settings import HOST, DOCTYPE, INDEX

def process_tags(parts):
    new_parts = []
    for part in parts:
        if part.strip(' \r\n\t') != '' and part.strip() != 'Related':
            new_parts.append(part)


    return ''.join(new_parts)


def get_page(url):
    # store the to-be-indexed document to item
    item = {
        'categories': [],
    }
    keywords = []

    page = requests.get(url)
    page.encoding = 'utf-8'
    html = etree.HTML(page.text)

    prev_url = html.xpath('//a[@rel="prev"]/@href')[0]
    title_parts = html.xpath('//h1//text()')
    # parts = html.xpath('//div[@class="entry-content"]//text()')
    content_parts = html.xpath('//div[@class="post-bodycopy cf"]//text()')
    categories = html.xpath('//a[@rel="category tag"]')

    item['url'] = url
    item['title'] = process_tags(title_parts)
    item['content'] = process_tags(content_parts)

    # Process the categories
    for category in categories:
        _cat = {}
        _cat['link'] = category.xpath('./@href')[0]
        _cat['name'] = category.xpath('./text()')[0]
        item['categories'].append(_cat)

    # Keywords
    keywords.append(item['title'])
    keywords.append(item['content'])
    keywords.extend([category['name'] for category in item['categories']])

    item['keywords'] = keywords

    return item, prev_url


def main():
    # url = u'https://blog.gslin.org/archives/2015/01/22/5548/backblaze-%E5%85%AC%E4%BD%88%E7%A1%AC%E7%A2%9F%E6%95%85%E9%9A%9C%E7%8E%87/'
    url = u'http://yychen.joba.cc/dev/archives/164'
    es = ElasticSearch(HOST)
    for i in range(20):
        item, url = get_page(url)

        # put it into es
        es.index(INDEX, DOCTYPE, doc=item, id=item['url'])


if __name__ == '__main__':
    main()
