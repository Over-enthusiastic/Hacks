#!/usr/bin/python

import subprocess
import sys
import csv
import string
from prettytable import PrettyTable
import operator

DUMP_FILE="contact.data"

mydict = {}

def check_adb_device() :
    x = subprocess.check_output(["./adb", "devices"]);
    #skip header and look for devices
    for l in x.split("\n")[1:] :
        if(l.find("device") > 0) :
            print("Found Device")
            return;
    print("No Devices Connected");
    sys.exit()

def get_contact_data(dump):
    print("Fetching data ....");
    data = subprocess.check_output(["adb", "shell" , "content", "query", "--uri content://com.android.contacts/data"],stderr=subprocess.STDOUT);
    fobj = open(dump,"w");
    fobj.write(data);
    fobj.close();

def find_key(keyvals, field):
    if keyvals.find("=") > 0:
        (key, val) =  keyvals.split("=")
        key = key.strip()
        if (key.strip() == field):
            print(val)
            return val.strip();
        else :
            return 0
    else : 
        return None

if __name__ == "__main__":
    check_adb_device();
    get_contact_data(DUMP_FILE);
    d = open(DUMP_FILE, "rb");
    i = 0;
    t = PrettyTable(['Name','contacted'])
    for l in d.readlines() :
        i = i+1
        val1 = ""
        val2 = ""
        for keyvals in l.split(","):
            s  = 'times_contacted';
            if keyvals.find("=") > 0:
                (key, val) =  keyvals.split("=")
                key = key.strip()
                if (key.strip() == s):
                    val2 = val.strip();
            s = 'display_name';
            if keyvals.find("=") > 0:
                (key, val) =  keyvals.split("=")
                key = key.strip()
                if (key.strip() == s):
                    val1 = val.strip();
        if(val1 != '' and val2 != '') :
            mydict[val1] = int(val2);
sorted_dict = sorted(mydict.items(),key=operator.itemgetter(1),reverse=True);
i=0;
for l in sorted_dict:
    i = i+1;
    t.add_row([l[0],l[1]])
    if( i > 11) :
        break;
print(t)
