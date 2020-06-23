#!/usr/bin/env python3
# adapted from code by @stephenhouser on github
# https://gist.github.com/stephenhouser/c5e2b921c3770ed47eb3b75efbc94799
from bs4 import BeautifulSoup
import requests
import re
import sys
import os
import http.cookiejar
import json
import urllib.request, urllib.error, urllib.parse
import bleach

def get_soup(url,header):
    return BeautifulSoup(urllib.request.urlopen(
        urllib.request.Request(url,headers=header)),
        'html.parser')

def bing_image_search(query):
    query = bleach.clean(query.lower())
    query= query.split()
    query='+'.join(query)
    url="http://www.bing.com/images/search?q=" + query + "&FORM=HDRSC2"

    #add the directory for your image here
    DIR="Pictures"
    header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    soup = get_soup(url,header)
    image_result_raw = soup.find("a",{"class":"iusc"})

    # if search request was successfull, but no results came up
    # then indicate no results found by -1 
    if not image_result_raw: 
        return -1
    m = json.loads(image_result_raw["m"])
    murl, turl = m["murl"],m["turl"]# mobile image, desktop image

    image_name = urllib.parse.urlsplit(murl).path.split("/")[-1]
    return (image_name,murl, turl)



if __name__ == "__main__":
    query = sys.argv[1]
    results = bing_image_search(query)
    print(results)