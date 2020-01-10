from flask import Flask

app = Flask(__name__)

from app import routes

#ef googlemap(*arg, **kwargs):
#	map = googlemap_obj(*args, **kwargs)
#	return Markup("",join((map.js, map.html
