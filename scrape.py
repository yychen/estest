#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from lxml import etree
from pyelasticsearch import ElasticSearch

from settings import HOST, DOCTYPE, INDEX


def process_tags(parts):
    # There may be empty text nodes extracted by lxml like \t\t\t\n\n\n
    # Take care of this part here
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
    page = requests.get(url)
    # page.encoding = 'utf-8'
    html = etree.HTML(page.text)

    try:
        prev_url = html.xpath('//a[@rel="prev"]/@href')[0]
    except IndexError:
        # We reached the end
        return None, None

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

    return item, prev_url


def main():
    # url = u'https://blog.gslin.org/archives/2015/01/22/5548/backblaze-%E5%85%AC%E4%BD%88%E7%A1%AC%E7%A2%9F%E6%95%85%E9%9A%9C%E7%8E%87/'
    url = u'http://yychen.joba.cc/dev/archives/164'
    es = ElasticSearch(HOST)
    for i in range(20):
        item, url = get_page(url)

        if not url:
            print '\033[1;33mWe\'ve reached the end, breaking...\033[m'
            break

        # put it into es
        print 'Indexing \033[1;37m%s\033[m (%s)...' % (item['title'], item['url'])
        es.index(INDEX, DOCTYPE, doc=item, id=item['url'])


if __name__ == '__main__':
    main()
