#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 22:24:50 2018

@author: phoenix
"""
import os
import shutil


class Utilities:
    def saveImageToDataset(self, image, name, dataset_path):
        #image = image path i.e. where on earth image is... 
        #name = name of the person...
        #dataset_path = path to dataset...
        dest = dataset_path + '/' + name
        list = [dir for root, dir, files in os.walk(dataset_path)]
        if name in list[0]:
            #no need to create folder
            shutil.copy2(image, dest)
            
        else:
            os.makedirs()
            shutil.copy2(image, dest)


    