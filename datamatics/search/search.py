from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Text, Document, Search
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from . import models


connections.create_connection()

class EmpIndex(Document):
    name = Text()
    code = Text()
    location = Text()

    class Index:
        name = 'employee-index'

def bulk_indexing():
    EmpIndex.init()
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing() for b in models.Employee.objects.all().iterator()))
