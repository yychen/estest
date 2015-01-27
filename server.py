#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import tornado.web
from tornado.ioloop import IOLoop
from pyelasticsearch import ElasticSearch

from settings import HOST, INDEX, DOCTYPE

es = ElasticSearch(HOST)


class SearchHandler(tornado.web.RequestHandler):
    def post(self):
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
            (r'/()$', tornado.web.StaticFileHandler, {'path': 'templates/index.html'}),
            (r'/search', SearchHandler),
        ],
        debug=True,
    )
    app.listen(9528)
    IOLoop.instance().start()


if __name__ == '__main__':
    main()
