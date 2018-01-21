#!/usr/bin/python3

import urllib3 
import json
import time
import sqlite3

#Change XYZ to a valid path
COOKIE_DB = "/home/aks/.mozilla/firefox/XYZ/cookies.sqlite"

def get_cookie() :
    name = []
    keyval = {}
    header = ''
    conn = sqlite3.connect(COOKIE_DB)
    conn1 = sqlite3.connect(COOKIE_DB)
    c = conn.cursor()
    c1 = conn1.cursor()
    c.execute('SELECT name FROM moz_cookies  where baseDomain = \'bookmyforex.com\' ')
    for n in c.fetchall() :
        c1.execute('SELECT value FROM moz_cookies  where baseDomain = \'bookmyforex.com\' and name = ?', n )
        n = n[0]
        val = c1.fetchone()[0]
        keyval[n] = val
    for key  in keyval :
        header += " %s=%s;"%(key,keyval[key])
    return header
    
def get_price(cookie) :
    #Feel free to change User-Agent
    request_header = {
        "Host": "www.bookmyforex.com",
        "User-Agent" : "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language" : "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.bookmyforex.com/",       
        "Connection": "keep-alive"
    }
    request_header ['Cookie'] = cookie
    http = urllib3.PoolManager()
    #BNG represents Bangalore, you can change to your city code in the json file
    req = http.request("GET","http://www.bookmyforex.com/api/secure/v1/get-full-rate-card?city_code=BNG", headers=request_header)
    data = json.loads(req.data)
    
    #Currently looks for only EUR , you can check other currency code in the json file
    for f in data['result'] :
        if ( f['currency_code'] == 'EUR' ) :
            #This is currently looking at sell for Forex card, can look for code in json for others
            return f['spc']

urllib3.disable_warnings()
price = 0;
base_time = time.time()
cookie  = get_cookie();
while( True ) :
    try:
        price_prev = price
        price = get_price(cookie)
        if (price_prev != price) :
            print( "%f : %s" %(time.time()-base_time , price))
        time.sleep(10.00)
    except  KeyboardInterrupt:
        print("Done")
        exit(0)
