#from app import app
from elasticsearch import Elasticsearch
from datetime import datetime

es = Elasticsearch()
es.index(index="my-index", doc_type="test-type", id=42, body={"any": "data", "timestamp": datetime.now()})
