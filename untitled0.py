#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 15:37:36 2018

@author: phoenix
"""

import glob

path = glob.glob('dataset/*')
for each in path:
    print(glob.glob(each+'/*')[0].split('/')[1])

dynamic_dict = { glob.glob(each+'/*')[0].split('/')[1]:glob.glob(each+'/*')[0] for each in path}
print(dynamic_dict) 