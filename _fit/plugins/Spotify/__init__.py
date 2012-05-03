import json
from os import path
with open(path.join(path.dirname(__file__), "descriptions.json")) as f:
	__descriptions__ = json.load(f)