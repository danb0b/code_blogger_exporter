# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 20:01:10 2019

@author: danaukes
"""

import yaml
import os
import sys
import glob

filename = '/home/danaukes/projects/project_embedded_systems_class/_source/blog-04-30-2021.xml'    
root_path,filename_stripped = os.path.split(filename)
export_folder = os.path.join(root_path,'export')
image_folder= os.path.join(export_folder,'figures')


files = glob.glob(os.path.join(root_path,'export/*.md'))

filenames = [os.path.splitext(item)[0] for item in files]
filenames = [os.path.split(item)[1] for item in filenames]

file_mapping = dict(zip(filenames,files))

with open(os.path.join(root_path,'categories.yaml')) as f:
    categories = yaml.load(f,Loader=yaml.FullLoader)
with open(os.path.join(root_path,'titles.yaml')) as f:
    titles = yaml.load(f,Loader=yaml.FullLoader)



for key,value in categories.items():    
    dict1 = {'tags':categories[key]}
    dict2 = {'title':titles[key]}
    with open(file_mapping[key],'r+') as f:
#        f.seek(0)
        content = f.read()
        f.seek(0)
        f.write('---\n'+yaml.dump(dict2)+yaml.dump(dict1)+'---\n'+content)
        