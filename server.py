# web client for barcode results
# shows list of what items were scanned
# by oran collins
# github.com/wisehackermonkey
# oranbusiness@gmail.com
# 20200623

# json database
# https://pypi.org/project/tinydb/

import json
from tinydb import TinyDB, Query
from bing_image_search import bing_image_search

DB_LOCATION = './server/db/db.json' 

db = TinyDB(DB_LOCATION)

# query_text = "MORTON SALT COMPANY 26 oz Morton Salt, Iodized"
# upc_code = "051138464646"
# result = bing_image_search(query_text)


# db.insert({'name': query_text,"image": result, "barcode": upc_code })


from flask import Flask
app = Flask(__name__)

@app.route("/api/v1/products")
def api():
    Barcodes = Query()
    barcode_info_json = db.search((Barcodes.barcode=="051138464646"))
    return json.jsonify(barcode_info_json)