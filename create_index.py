#!/usr/bin/env python
from pyelasticsearch import ElasticSearch
from pyelasticsearch.exceptions import ElasticHttpNotFoundError

from settings import HOST, INDEX, DOCTYPE

index_settings = {
    'mappings': {
        DOCTYPE: {
            'properties': {
                # 'title': {'type': 'string', 'index': 'not_analyzed'},
                'title': {'type': 'string', 'analyzer': 'mmseg', 'boost': 1.5, 'term_vector': 'with_positions_offsets'},
                'url': {'type': 'string', 'index': 'not_analyzed'},
                # 'content': {'type': 'string', 'index': 'not_analyzed'},
                'content': {'type': 'string', 'analyzer': 'mmseg', 'boost': 0.7, 'term_vector': 'with_positions_offsets'},
                'categories': {'type': 'nested',
                    'properties': {
                        'url': {'type': 'string', 'index': 'not_analyzed'},
                        'name': {'type': 'string', 'index': 'not_analyzed'},
                    }
                }
            }
        }
    }
}

es = ElasticSearch(HOST)
try:
    es.delete_index(INDEX)
except ElasticHttpNotFoundError:
    # No index found
    pass

es.create_index(INDEX, settings=index_settings)
