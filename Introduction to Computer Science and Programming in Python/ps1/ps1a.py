#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 13:34:45 2023

@author: angelcruz
"""

annual_salary = float(input("Enter your annual salary: "))
portion_saved = float(input("Enter the percentage of your salary to save, as a decimal: "))
total_cost = float(input("Enter the cost of your dream home: "))

r = 0.04 #annual rate
portion_down_payment = 0.25 #portion of the cost needed for downpayment
current_savings, months = 0, 0

while(current_savings <= total_cost*portion_down_payment):
    months+=1
    current_savings*= (1 + r/12)
    current_savings+= (annual_salary/12)*portion_saved
  
    
print("Number of months: ", months)