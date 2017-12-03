#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 20:43:39 2017

@author: sunkaiman
"""
import numpy as np
class trading_strategy:
    def __init__(self):
        self.ma_5 = 0
        self.ma_25 = 0
        self.pnl = [0]
        self.price_list = []
        self.position = 0
        self.cost = 0

    def check_signal(self):
        if self.ma_5>self.ma_25 and self.position == 0:
            return 1
        elif self.ma_5<self.ma_25 and self.position == 1:
            return -1

    def update_pnl(self,p,signal):
        if signal == 1:
            self.cost = p
            self.pnl.append(self.pnl[-1])
            self.position = 1      
        elif signal == -1:
            temp = self.pnl[-1]+p-self.cost
            self.pnl.append(temp)
            self.position = 0

    def process_tick(self, adjusted_price):
        p = adjusted_price[1]
        d = adjusted_price[0]
        self.price_list.append(p)
        if len(self.price_list)>25:
            self.ma_5 = np.mean(self.price_list[-5:])
            self.ma_25 = np.mean(self.price_list[-25:])
            signal = self.check_signal()
            if signal == 1:
                self.generate_buy_order(p,d)
            elif signal ==-1:
                self.generate_sell_order(p,d)
            self.update_pnl(p,signal)
        else:
            pass
        
    def generate_buy_order(self, p, d):
        print('BUY: {0}, {1}'.format(p, d.strftime('%Y-%m-%d')))
    
    def generate_sell_order(self, p, d):
        print('SELL: {0}, {1}'.format(p, d.strftime('%Y-%m-%d')))
        
    def display_pnl(self):
        print('Final PNL: {}'.format(self.pnl[-1]))