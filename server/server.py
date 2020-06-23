# web client for barcode results
# shows list of what items were scanned
# by oran collins
# github.com/wisehackermonkey
# oranbusiness@gmail.com
# 20200623

# json database
# https://pypi.org/project/tinydb/
#%%
from tinydb import TinyDB, Query
db = TinyDB('./server/db/db.json')
db.insert({'int': 1, 'char': 'a'})
db.insert({'int': 1, 'char': 'b'})