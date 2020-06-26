#!/usr/bin/python3

# barcode-item-tracker
# raspberry pi database that connects and tracks items entered useing a barcode scanner

# by oran collins
# github.com/wisehackermonkey
# oranbusiness@gmail.com
# 20200622

# Code addapted from this post
# Posted on Aug 20 2017 - 4:39am by piddler
# https://www.piddlerintheroot.com/barcode-scanner/


import sys
import os
import requests
import json


# module to turn product name into a photo using bing image search
from bing_image_search import bing_image_search
# load api key from .env file
# more info on how to use .env files
# https://pypi.org/project/python-dotenv/ 
from dotenv import load_dotenv
load_dotenv()

from tinydb import TinyDB, Query
DB_LOCATION = './server/db/db.json' 

# database setup
db = TinyDB(DB_LOCATION)


api_key = os.getenv("API_KEY") #https://upcdatabase.org/

def barcode_reader(usb_port):
    """Barcode code obtained from 'brechmos' 
    https://www.raspberrypi.org/forums/viewtopic.php?f=45&t=55100"""
    hid = {4: 'a', 5: 'b', 6: 'c', 7: 'd', 8: 'e', 9: 'f', 10: 'g', 11: 'h', 12: 'i', 13: 'j', 14: 'k', 15: 'l', 16: 'm',
           17: 'n', 18: 'o', 19: 'p', 20: 'q', 21: 'r', 22: 's', 23: 't', 24: 'u', 25: 'v', 26: 'w', 27: 'x', 28: 'y',
           29: 'z', 30: '1', 31: '2', 32: '3', 33: '4', 34: '5', 35: '6', 36: '7', 37: '8', 38: '9', 39: '0', 44: ' ',
           45: '-', 46: '=', 47: '[', 48: ']', 49: '\\', 51: ';', 52: '\'', 53: '~', 54: ',', 55: '.', 56: '/'}

    hid2 = {4: 'A', 5: 'B', 6: 'C', 7: 'D', 8: 'E', 9: 'F', 10: 'G', 11: 'H', 12: 'I', 13: 'J', 14: 'K', 15: 'L', 16: 'M',
            17: 'N', 18: 'O', 19: 'P', 20: 'Q', 21: 'R', 22: 'S', 23: 'T', 24: 'U', 25: 'V', 26: 'W', 27: 'X', 28: 'Y',
            29: 'Z', 30: '!', 31: '@', 32: '#', 33: '$', 34: '%', 35: '^', 36: '&', 37: '*', 38: '(', 39: ')', 44: ' ',
            45: '_', 46: '+', 47: '{', 48: '}', 49: '|', 51: ':', 52: '"', 53: '~', 54: '<', 55: '>', 56: '?'}

    fp = open(usb_port, 'rb')

    ss = ""
    shift = False

    done = False

    while not done:

        ## Get the character from the HID
        buffer = fp.read(8)
        for c in buffer:
            if c > 0:

                ##  40 is carriage return which signifies
                ##  we are done looking for characters
                if int(c) == 40:
                    done = True
                    break;

                ##  If we are shifted then we have to
                ##  use the hid2 characters.
                if shift:

                    ## If it is a '2' then it is the shift key
                    if int(c) == 2:
                        shift = True

                    ## if not a 2 then lookup the mapping
                    else:
                        ss += hid2[int(c)]
                        shift = False

                ##  If we are not shifted then use
                ##  the hid characters

                else:

                    ## If it is a '2' then it is the shift key
                    if int(c) == 2:
                        shift = True

                    ## if not a 2 then lookup the mapping
                    else:
                        ss += hid[int(c)]
    return ss

def UPC_lookup(api_key,upc):
    '''V3 API'''

    if os.getenv("UPC_PROVIDER") == "barcodelookup":#select which website to use for upc lookup barcodelookup.com
        return barcodelookup(api_key, upc)
    elif os.getenv("UPC_PROVIDER") == "upcdatabase":# or upcdatabase.com
        return upcdatabase(api_key, upc)

def upcdatabase(api_key,upc):
    url = "https://api.upcdatabase.org/product/{}?apikey={}".format(upc,api_key)
    print(url)

    headers = {
        'cache-control': "no-cache",
    }

    response = requests.request("GET", url, headers=headers)

    json_result = response.json()
    

    if json_result["success"]:
        description, images, brand = json_result["description"], json_result["images"], json_result["brand"]
        return (description, images, brand)
    else:
        print(json_result["error"])
        print("UPC: not found")  
        return -1     
    print("-----" * 5 + "\n")
def barcodelookup(api_key, upc):
    url = f"https://api.barcodelookup.com/v2/products?barcode={upc}&formatted=y&key={api_key}"
    response = requests.request("GET", url)
    json_result = response.json()
    # if barcodelookup.com found a match for the upc code
    if json_result:
        product = json_result["products"][0]
        
        print( product)
        description, image = product["product_name"], product["images"][0]
        print(description)
        print(image)
        return (description, image, "None")
    else:
        print(json_result["error"])
        print("UPC: not found") 
        return -1

    

     

if __name__ == '__main__':
    print("Usb Barcode Database: Running..")
    print("Please scan a item now")
    try:
        while True:
            # 1) read the barcode from usb barcode reader
            upc = barcode_reader('/dev/hidraw1')
            # 2) look up barcode number for product name
            results = UPC_lookup(api_key,upc)
            # doent do anything if not found
            if results == -1:
                continue
            description, image, brand = results

            # 3) find image that matches product, if upc api doesnt find one 
            if not image:  
                image = bing_image_search(description)
                # if bing image search didnt find any images
                if image == -1:
                    image = "Image Not found"
            # 3) show results 
            print("-----" * 5)
            print("UPC: {}\n{}\n{}\n{}".format(upc,description, image, brand))
            db.insert({'name': description,"image": image, "barcode": upc })
            print("-----" * 5)

    except KeyboardInterrupt:
        pass