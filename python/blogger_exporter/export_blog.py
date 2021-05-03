# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 13:01:08 2019

@author: daukes
"""
import time
import os
import sys
import requests
import PIL
import PIL.Image
import shutil

imtypemapping= {'jpeg':'jpg','png':'png'}

def cleantext(text_in):
    text_out = "".join([c for c in text_in if c.isalpha() or c.isdigit() or c==' ']).rstrip()
    text_out=text_out.replace(' ','-')
    text_out=text_out.lower()
    return text_out


def printattrs(item):
    for item2 in dir(item):
        print(getattr(item,item2))

def get_children(root):
    children = []
    searchlist = [root]
    
    while not not searchlist:
        item=searchlist.pop(0)
        items = item.getchildren()
        searchlist.extend(items)
        children.extend(items)
    return children

def get_post_html(post):
    item = post.find('{http://www.w3.org/2005/Atom}content')
    text = item.text
    textb = text.encode('utf-8')
    root2 = et.HTML(textb)
    return root2    
    

#filename = 'blog-09-05-2019.xml'
#filename = 'blog-12-27-2019.xml'    
# filename = 'blog-12-30-2019.xml'    
filename = '/home/danaukes/projects/project_embedded_systems_class/_source/blog-04-30-2021.xml'    
root_path,filename_stripped = os.path.split(filename)
export_folder = os.path.join(root_path,'export')
image_folder= os.path.join(export_folder,'figures')

    
with open(filename,'rb') as f:
    output = f.readlines()

output=b''.join(output)


import lxml.etree as et
import lxml.html as html

root = et.XML(output)
#c = root.getchildren()[0]

children = get_children(root)    
childtags = [item.tag for item in children]
#print(childtags)
#

posts = []
for ii,item in enumerate(children):
    if 'entry' in item.tag:
#        print(item.tag)
        cat = item.find('{http://www.w3.org/2005/Atom}category')
#        print(cat.attrib['term'])
        if cat.attrib['term'] =='http://schemas.google.com/blogger/2008/kind#post':
            posts.append(item)
#        for item2 in item.getchildren():
#            try:
#                print('  '+item2.text)
#            except TypeError:
#                pass
#        break
        
#        print(cat.text)
#c=children[ii]    
#c2 = c.find('{http://www.w3.org/2005/Atom}category')
#
#printattrs(c2)


titles = []
        
#for post in children:
#    for item in post:
#        if 'title' in item.tag.lower():
#            titles.append(item.text)

#titles.sort()
#print(titles)

posts = []
            
for item in children:
    
    if 'category' in item.tag.lower():
#        print(item.tag)
        if 'term' in item.attrib:
            if 'post' in item.attrib['term'].lower():
                posts.append(item.getparent())
#                print(item.getparent())
                
#print(entries)
                
#                title
for post in posts:
    title = None
    for item in post:
        if 'title' in item.tag.lower():
            title = item.text
    if title is None:
        print(post)
    else:
        print(title)
    titles.append(title)
#        else:
#            print(item)
    
images = []
for post in posts:
    root2 = get_post_html(post)
    children2=get_children(root2)
    my_images = []
    for item in children2:
        try:
            tag = item.tag
            if tag.lower()=='img':
                my_images.append(item)
        except AttributeError:
            pass
#    my_images = [item for item in children2 if (item.tag).lower()=='img']
    images.extend(my_images)
#print(images)

srcs = [item.attrib['src'] for item in images]    
srcs = list(set(srcs))
mapping = []
for ii,item in enumerate(srcs):
    ftype = os.path.splitext(item)[1].lower()
    mapping.append([item,'figure_{0:03.0f}{1:s}'.format(ii,ftype)])
    
#fnames = [os.path.split(item)[1] for item in srcs]
#fnames.sort()


if os.path.exists(export_folder):
    shutil.rmtree(export_folder)
time.sleep(1)
os.mkdir(export_folder)
os.mkdir(image_folder)

errors = []

for ii,(key,value) in enumerate(mapping):
    try:
        r = requests.get(key) # create HTTP response object 
        if r.ok:
            with open(os.path.join(image_folder,value),'wb') as f: 
                f.write(r.content)     
            img = PIL.Image.open(os.path.join(image_folder,value))
            itype = imtypemapping[img.format.lower()]
            del img
            froot,ctype = os.path.splitext(value)
            new = froot+'.'+itype.lower()
            os.rename(os.path.join(image_folder,value),os.path.join(image_folder,froot+'.'+itype.lower()))
            mapping[ii][1] = new
        else:
            errors.append(('404',key,value))
    except requests.exceptions.InvalidSchema as e:
        errors.append((e,key,value))
        

mapping_fwd = dict([tuple(item) for item in mapping])
    
for post,title in zip(posts,titles):
    item = post.find('{http://www.w3.org/2005/Atom}content')
    text = item.text
    textb = text.encode('utf-8')
    root2 = et.HTML(textb)
    children2=get_children(root2)
    for item in children2:
        try:
            tag = item.tag
            if tag.lower()=='img':
                item.attrib['src']='figures/'+mapping_fwd[item.attrib['src']]
        except AttributeError:
            pass
    textb2 = et.tostring(root2, pretty_print=True)
    filename = cleantext(title)
    with open(os.path.join(export_folder,filename+'.html'),'wb') as f:
#        f.writelines(textb)
        f.write(textb2)
        
import yaml
with open(os.path.join(root_path,'404.yml'),'w') as f:
    yaml.dump(errors,f)