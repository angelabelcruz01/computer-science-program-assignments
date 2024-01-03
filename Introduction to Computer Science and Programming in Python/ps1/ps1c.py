#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 15:00:07 2023

@author: angelcruz
"""

annual_salary_init = float(input("Enter your starting annual salary: "))

total_cost = 1000000
semi_annual_raise = 0.07
r = 0.04 #annual rate
portion_down_payment = 0.25 #portion of the cost needed for downpayment
current_savings = 0
months = 36
low, high = 0, 10000
steps, portion_saved = 0, 0

while abs(current_savings - total_cost*portion_down_payment) > 100:
    steps+=1
    
    annual_salary = annual_salary_init
    current_savings = 0
    portion_saved = (low + high)/2
    
    if portion_saved == 10000:
        print('It is not possible to pay the downpayment in three years')
        break
    
    else:        
        for m in range(1,months+1,1):
            current_savings*= (1 + r/12)
            current_savings+= (annual_salary/12)*(portion_saved/10000) 
        
            if(m%6 == 0):
                annual_salary*= (1+semi_annual_raise)
            else:
                None
                
        if current_savings < total_cost*portion_down_payment:
            low = portion_saved
        elif current_savings > total_cost*portion_down_payment:
            high = portion_saved
        else:
            break
    

  
if portion_saved == 10000:
     None
else:
    print("Best savings rate: ", portion_saved/10000)
    print("Steps in bisection search: ", steps)