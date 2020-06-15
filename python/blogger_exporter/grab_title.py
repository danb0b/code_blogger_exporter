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
import yaml

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
filename = 'blog-12-30-2019.xml'    
    
    
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
#
#posts = []
#for ii,item in enumerate(children):
#    if 'title' in item.tag:
#        
#        print(item.tag)
#        cat = item.find('{http://www.w3.org/2005/Atom}category')
##        print(cat.attrib['term'])
#        if cat.attrib['term'] =='http://schemas.google.com/blogger/2008/kind#post':
#            posts.append(item)
##        for item2 in item.getchildren():
##            try:
##                print('  '+item2.text)
##            except TypeError:
##                pass
##        break
        
#        print(cat.text)
#c=children[ii]    
#c2 = c.find('{http://www.w3.org/2005/Atom}category')
#
#printattrs(c2)


filenames = []
        
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
                
titles = []
                
#                title
for post in posts:
    filename = None
    title = None
    for item in post:
        if 'title' in item.tag.lower():
            filename = item.text
            title = item.text
    if filename is None:
        print(post)
    else:
        print(filename)
    filename = cleantext(filename)
    filenames.append(filename)
    titles.append(title)
#        else:
#            print(item)

mapping = []

for p,filename,title in zip(posts,filenames,titles):
#    category_children = p.findall('{http://www.w3.org/2005/Atom}category')
#    categories = [child.attrib['term'] for child in category_children]
#    categories = [item for item in categories if 'schema' not in item]
#    categories = [item.lower() for item in categories]
    mapping.append((filename,title))

mapping = dict(mapping)

with open('titles.yaml','w') as f:
    yaml.dump(mapping,f)
#    
#for post,filename in zip(posts,filenames):
#    item = post.find('{http://www.w3.org/2005/Atom}content')
#    text = item.text
#    textb = text.encode('utf-8')
#    root2 = et.HTML(textb)
#    children2=get_children(root2)
#    for item in children2:
#        try:
#            tag = item.tag
#            if tag.lower()=='img':
#                item.attrib['src']='figures/'+mapping_fwd[item.attrib['src']]
#        except AttributeError:
#            pass
#    textb2 = et.tostring(root2, pretty_print=True)
#    with open('export/'+filename+'.html','wb') as f:
##        f.writelines(textb)
#        f.write(textb2)