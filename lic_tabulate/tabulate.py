#!/usr/bin/python

''' 
LIC policy analytics
-----------------------
Aim of the application : 
 Calculate following figures for a given insurance policy :
 1) year on year benefit in %
 2) Bonus in absolute numbers
 3) Current expected returns
 4) Date of Next payment and number of terms left


This piece of python code can parse a json file that
contains details about LIC. Following is a simple
example of a json file that can be fed to this code.

LIC.json
--------
{
 "policies" : [
	{  "premium": 4830, "policy_number": 20610034162500000000,  "sum_assured": 300000,"policy_type": "Mediclaim", "inception": "2016-11-26", "last_payment": "2017-11-26" },
	{  "premium": 29761, "policy_number": 66000005,  "sum_assured": 800000,"policy_type": "LIC Jeevan Anand (P&AB)", "inception": "2013-9-28", "last_payment": "2038-9-28" }
 ]
}

OUTPUT :

+----------------------+--------------+---------+------------+--------------+---------------+-------------+-------------+----------+----------+
|      Policy no       | Sum assured  | Premium |   incpt    | Payment left | Total Payment |    bonus    |     Net     |   Net%   |   y2y    |
+----------------------+--------------+---------+------------+--------------+---------------+-------------+-------------+----------+----------+
| 20610034162500000000 | 3,00,000.00  |   4830  | 2016-11-26 |     0.00     |    9,660.00   |     0.00    | 3,00,000.00 | 3105.59% | 3005.59% |
|    66000005          | 8,00,000.00  |  29761  | 2013-09-28 | 6,24,981.00  |  7,73,786.00  | 1,17,600.00 | 9,17,600.00 | 118.59%  |  0.68%   |
+----------------------+--------------+---------+------------+--------------+---------------+-------------+-------------+----------+----------+


'''

from prettytable import PrettyTable as pt
from datetime import date 
import locale
import json
from pprint import pprint
import codecs

bonus_2020 = { 11:34 ,15:37 ,20:41 ,100:45 }
bonus_2019 = { 5:34 , 11:34, 15:37 ,20:41, 100:45 }
bonus_2018 = { 11:38 ,15:41 ,20:45 ,100:49 }
bonus_2014 = { 11:37, 15:40 ,20:44, 100:48 }
bonus_2012 = { 11:36, 15:39 ,20:43, 100:47 }
bonus_2010 = { 11:34, 15:37 ,20:41, 100:45 }
bonus_2006 = { 11:32, 15:36 ,20:40, 100:44 }
bonus_2005 = { 5:30 , 11:34, 15:38 ,20:43, 100:47 }
bonus_2004 = { 5:34 , 11:38, 15:43 ,20:49, 100:53 }
bonus = { 
          2005:bonus_2005 ,
          2006:bonus_2006 ,
          2007:bonus_2010 ,
          2008:bonus_2010 ,
          2009:bonus_2010 ,
          2010:bonus_2010 ,
          2011:bonus_2012 ,
          2012:bonus_2012 ,
          2013:bonus_2014 ,
          2014:bonus_2014 ,
          2015:bonus_2018 ,
          2016:bonus_2018 ,
          2017:bonus_2018 ,
          2018:bonus_2018 ,
          2019:bonus_2019 ,
          2020:bonus_2020 ,
	#predict the future
          #2021:bonus_2020 ,
          #2022:bonus_2020 ,
          #2023:bonus_2020 ,
          #2025:bonus_2020 ,
          #2026:bonus_2020 ,
          #2027:bonus_2020 ,
          #2028:bonus_2020 ,
          #2029:bonus_2020 ,
          #2030:bonus_2020 ,
          }
def print_money(x) :
    return locale.currency(x, grouping=True,symbol=False)
def print_percent(x) :
    return '{0:.2f}'.format(x)+'%'

class insurance_policy(object)  :
    policy_number = int();
    policy_type = str();
    premium = 0;
    inception = date(1,1,1);
    sum_assured =  int()
    last_payment = date(1,1,1);
    nr_years = 0;
    years_left = 0;
    payment_tilldate = 0;
    payment_left = 0;
    payment_total = 0;
    payment_percent = 0;
    profit = 0;
    bonus = 0;
    net = 0;
    net_percent = 0;
    y2y = 0;
    def __init__(self):
        pass
    def evaluate(self) :
        self.nr_years = ((self.last_payment -  self.inception).days/365) +1
        self.years_left = 1+(self.last_payment-date.today()).days/365 ;
        if ( self.years_left < 0 ) : self.years_left = 0;
        self.payment_total =  self.nr_years * self.premium;
        self.payment_left =  self.years_left * self.premium;
        self.payment_percent = ((100.0*self.years_left) /self.nr_years);
        self.profit =   ((self.sum_assured*100.0)/self.payment_total)
        for key in bonus : 
            if (key > (self.inception.year + 1)) and ( key < self.last_payment.year) :
                year = key ; 
                for key in bonus[key] :
                    if (key > self.nr_years) :
                        self.bonus += bonus[year][key]*(self.sum_assured/1000);
        self.net = (self.bonus+self.sum_assured);
        self.net_percent = (self.net *100.0 /self.payment_total)
        y2y = (self.net_percent/100) ** (1.00/(self.nr_years-1))
        self.y2y = ( y2y -1 ) * 100

    def create_row(self):
        sa = print_money(self.sum_assured);
        pt = print_money(self.payment_total);
        pl = print_money(self.payment_left);
        incpt = date.isoformat(self.inception)
        lst_pay = date.isoformat(self.last_payment)
        x = [ self.policy_type, str(self.policy_number) , sa , self.premium , incpt, self.nr_years, self.years_left , pl , pt,  print_percent(self.payment_percent) , print_percent(self.profit), print_money(self.bonus), print_money(self.net),print_percent(self.net_percent), print_percent(self.y2y)];
        return x;

def extract_date(x) :
    (yyyy, mm ,dd) = x.split('-')
    return date(int(yyyy),int(mm),int(dd))
    

#define locale for print formats
locale.setlocale(locale.LC_MONETARY, 'en_IN')

#globals 
all_polcies = []

x = pt(['Type' ,'Policy no', 'Sum assured', 'Premium','incpt','Yrs' , 'left' , 'Payment left' , 'Total Payment', '% left', '% profit', 'bonus', 'Net', 'Net%', 'y2y'])

data_file = codecs.open("LIC.json", "r", "utf-8") 
data = json.load(data_file)
for item in data['policies'] :
    p = insurance_policy()
    p.policy_type = item["policy_type"]
    p.policy_number = item [ 'policy_number' ]
    p.premium = item['premium']
    p.sum_assured = item['sum_assured']
    p.inception = extract_date(item['inception'])
    p.last_payment = extract_date(item['last_payment'])
    p.evaluate()
    all_polcies.append(p)
    x.add_row(p.create_row())

p = insurance_policy()
for plcy in all_polcies :
    if ( plcy.policy_type.find('LIC') != -1) :
        p.sum_assured += plcy.sum_assured;
        p.payment_left += plcy.payment_left;
        p.payment_total += plcy.payment_total;
        p.premium += plcy.premium;
        p.bonus += plcy.bonus;
        if (p.last_payment <  plcy.last_payment) :
            p.last_payment = plcy.last_payment;
    p.premium += plcy.premium;

p.policy_type = 'Total'
p.policy_number = ''
p.profit = ((p.sum_assured*100.0)/p.payment_total)
x.add_row(p.create_row())

print (x)
print (x.get_string(fields=["Policy no", "Sum assured", "Premium","incpt","Payment left","Total Payment", "bonus", "Net", "Net%", 'y2y'])) 
