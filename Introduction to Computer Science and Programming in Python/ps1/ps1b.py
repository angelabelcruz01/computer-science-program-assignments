#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 14:08:10 2023

@author: angelcruz
"""

annual_salary = float(input("Enter your starting annual salary: "))
portion_saved = float(input("Enter the percentage of your salary to save, as a decimal: "))
total_cost = float(input("Enter the cost of your dream home: "))
semi_annual_raise = float(input("Enter the semi-annual raise, as a decimal: "))

r = 0.04 #annual rate
portion_down_payment = 0.25 #portion of the cost needed for downpayment
current_savings, months = 0, 0

while(current_savings <= total_cost*portion_down_payment):
    months+=1
    current_savings*= (1 + r/12)
    current_savings+= (annual_salary/12)*portion_saved 
    
    if(months%6 == 0):
        annual_salary*= (1+semi_annual_raise)
    else:
        None
  
    
print("Number of months: ", months)