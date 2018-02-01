#! /bin/env python
import urllib3 
import json
import time
import sqlite3

#Change XYZ with your mozilla profile id
COOKIE_DB = "/home/aks/.mozilla/firefox/XYZ/cookies.sqlite"
#Change this to your spliwise group name
SPLITWISE_GROUP_NAME = "somename"


def get_cookie() :
    name = []
    keyval = {}
    header = ''
    conn = sqlite3.connect(COOKIE_DB)
    conn1 = sqlite3.connect(COOKIE_DB)
    c = conn.cursor()
    c1 = conn1.cursor()
    c.execute('SELECT name FROM moz_cookies  where baseDomain = \'splitwise.com\' ')
    for n in c.fetchall() :
        c1.execute('SELECT value FROM moz_cookies  where baseDomain = \'splitwise.com\' and name = ?', n )
        n = n[0]
        val = c1.fetchone()[0]
        keyval[n] = val
    for key  in keyval :
        header += " %s=%s;"%(key,keyval[key])
    return header
    
def get_price(cookie) :
    request_header = {
        "Host": "secure.splitwise.com",
        "User-Agent" : "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language" : "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://secure.splitwise.com/",       
        "Connection": "keep-alive"
    }
    request_header ['Cookie'] = cookie
    http = urllib3.PoolManager()
    req = http.request("GET","http://secure.splitwise.com/api/v3.0/get_main_data?no_expenses=1&limit=3&cachebust=0.9212128862095217", headers=request_header)
    data  = json.loads(req.data)
    return data;

urllib3.disable_warnings()
data = get_price(get_cookie())

for x in data['groups'] :
    if (x['name'] == SPLITWISE_GROUP_NAME) :
        for y in x['simplified_debts'] :
                print(y['amount'])
