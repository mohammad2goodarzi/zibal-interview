from pymongo import MongoClient


# TODO: it's better to be a environment variable
url = 'mongodb://localhost:27017'
client = MongoClient(url)

# TODO: it's better to be a environment variable too
db = client['default']
