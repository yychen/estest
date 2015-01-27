#!/usr/bin/env python
from pyelasticsearch import ElasticSearch

from settings import HOST, INDEX, DOCTYPE


es = ElasticSearch(HOST)
results = es.search('*:*', index=INDEX, doc_type=DOCTYPE)
hits = results['hits']['hits']
print hits
