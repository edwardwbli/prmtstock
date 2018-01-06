#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import tushare as ts
import pandas as pd
import requests

IFTTT_KEY = ['xxxxxx'] #The IFTTT Key for your API
PORTFOLIOS = ['601398','000001'] #Stock Number list
START = 0 # starting point of stock price record 
END = 3 # ending point of stock price record

#IFTTT event 
API_STOCK_RISING = 'stock_rising' 
API_STOCK_FALLING = 'stock_falling'

def get_portfolios_p_change(portfolios, start, end):
    
    portfolios_change = pd.DataFrame()
    for stock in portfolios:
        stock_change= ts.get_hist_data(stock)[start:end].loc[:, ['p_change']]
        stock_change.columns=[stock]
        portfolios_change = pd.concat([portfolios_change, stock_change], axis=1) 

    print(portfolios_change)
    return portfolios_change

def get_rising_portfolios (portfolios) :
    return portfolios[portfolios > 0].dropna(axis=1, how='any')

def get_falling_portfolios (portfolios) :
    return portfolios[portfolios < 0].dropna(axis=1, how='any')

def notify_ifttt(payload,api):
    #ifttt webhooks api https://maker.ifttt.com/trigger/stock_rising/with/key/<your api key>
    data = {"value1" : payload}
    for user in IFTTT_KEY:
        requests.post('https://maker.ifttt.com/trigger/' + api + '/with/key/' + user, data = data)
    
if __name__ == '__main__':
    portfolios = get_portfolios_p_change(PORTFOLIOS,START,END)

    #get rising portfolios, and notify user
    portfolios_rising = get_rising_portfolios(portfolios)
    if not portfolios_rising.empty: 
        notify_ifttt(portfolios_rising.columns.values,API_STOCK_RISING) 

    #get falling portfolios, and notify user
    portfolios_falling = get_falling_portfolios(portfolios)
    if not portfolios_falling.empty:
        notify_ifttt(portfolios_falling.columns.values,API_STOCK_FALLING)
