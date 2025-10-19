import os
from elasticsearch import Elasticsearch

ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST", "elasticsearch")
ELASTICSEARCH_PORT = int(os.getenv("ELASTICSEARCH_PORT", 9200))

es = Elasticsearch(
    hosts=[{
        "host": ELASTICSEARCH_HOST,
        "port": ELASTICSEARCH_PORT,
        "scheme": "http"   # <-- ekhane scheme specify kora lagbe
    }],
    verify_certs=False
)
