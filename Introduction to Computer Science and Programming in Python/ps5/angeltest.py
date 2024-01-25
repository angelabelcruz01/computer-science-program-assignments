#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 20:59:24 2024

@author: angelcruz
"""


from datetime import datetime

ancient = datetime(1987, 10, 15)
input_datetime = datetime.strptime("3 Oct 2016 17:00:10", "%d %b %Y %H:%M:%S")

print(ancient, '\n', input_datetime)
print(ancient == input_datetime)
