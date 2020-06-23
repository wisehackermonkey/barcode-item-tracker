# web client for barcode results
# shows list of what items were scanned
# by oran collins
# github.com/wisehackermonkey
# oranbusiness@gmail.com
# 20200623

# json database
# https://pypi.org/project/tinydb/


from flask import Flask

from flask import jsonify
from flask import render_template 

from tinydb import TinyDB, Query
from bing_image_search import bing_image_search

from dotenv import load_dotenv
load_dotenv()

DB_LOCATION = './server/db/db.json' 

# database setup
db = TinyDB(DB_LOCATION)

# flask webserver setup
app = Flask(__name__)

# query_text = "MORTON SALT COMPANY 26 oz Morton Salt, Iodized"
# upc_code = "051138464646"
# result = bing_image_search(query_text)


# db.insert({'name': query_text,"image": result, "barcode": upc_code })




@app.route("/")
def main_page():
    Barcodes = Query()
    products = db.search((Barcodes.barcode.exists()))
    return render_template('index.html', products=products)

@app.route("/api/v1/products/all")
def api_all():
    Barcodes = Query()
    products = db.search((Barcodes.barcode.exists()))
    return jsonify(barcode_info_json)


# run the application
if __name__ == "__main__":
    # add if development or production .env
    app.run(debug=True)