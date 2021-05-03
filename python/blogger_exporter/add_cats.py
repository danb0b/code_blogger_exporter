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

with open(os.path.join(root_path,'page_info.yaml')) as f:
    page_info = yaml.load(f,Loader=yaml.FullLoader)

for key,value in page_info.items():    
    with open(file_mapping[key],'r+') as f:
        content = f.read()
        f.seek(0)
        f.write('---\n'+yaml.dump(page_info[key])+'---\n'+content)
        