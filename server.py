#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
import json
import logging
import hashlib
import cStringIO
from datetime import datetime, timedelta

import tornado.web
from tornado.ioloop import IOLoop
from jinja2 import Environment, FileSystemLoader
from pyelasticsearch import ElasticSearch

from settings import HOST, INDEX, DOCTYPE

env = Environment(loader=FileSystemLoader('templates'))
es = ElasticSearch(HOST)


def render(handler, template_name, arguments=None):
    template = env.get_template(template_name)

    if arguments:
        kwargs = arguments.copy()
    else:
        kwargs = {}
    handler.write(template.render(**kwargs))


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        render(self, 'index.html')

    def post(self):
        print self.get_argument('q')
        '''
        keywords = self.get_argument('q').split(' ')
        dsl = {
            'query': {},
            'filter': {
                'or': []
            }
        }

        for keyword in keywords:
            dsl['filter']['or'].append({
                'term': {'keyword': keyword}
            })
        '''
        dsl = {
            'query': {
                'bool': {
                    'should': [
                        {'match': {'content': self.get_argument('q')}},
                        {'match': {'title': self.get_argument('q')}},
                    ]
                }
            },
            'highlight': {
                'pre_tags': ['<em>'],
                'post_tags': ['</em>'],
                'fields': {
                    'content': {'no_match_size': 150, 'number_of_fragments': 1},
                    'title': {'no_match_size': 150, 'number_of_fragments': 0},
                }
            }
        }

        results = es.search(dsl, index=INDEX, doc_type=DOCTYPE)
        hits = results['hits']['hits']
        self.write(json.dumps(hits))


def main():
    app = tornado.web.Application(
        [
            (r'/', IndexHandler),
        ],
        static_path='static',
        debug=True,
    )
    app.listen(9528)
    IOLoop.instance().start()


if __name__ == '__main__':
    main()
