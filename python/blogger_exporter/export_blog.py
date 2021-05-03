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


def get_posts(children):
    
    posts = []
    
    for item in children:
        if 'category' in item.tag.lower():
            if 'term' in item.attrib:
                if 'post' in item.attrib['term'].lower():
                    posts.append(item.getparent())

    return posts

def get_categories(post):
    category_children = p.findall('{http://www.w3.org/2005/Atom}category')
    categories = [child.attrib['term'] for child in category_children]
    categories = [item for item in categories if 'schema' not in item]
    categories = [item.lower() for item in categories]
    return categories

if __name__=='__main__':
        
    
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
    
    children = get_children(root)    
    childtags = [item.tag for item in children]
    
    # posts = []
    # for ii,item in enumerate(children):
    #     if 'entry' in item.tag:
    #         cat = item.find('{http://www.w3.org/2005/Atom}category')
    #         if cat.attrib['term'] =='http://schemas.google.com/blogger/2008/kind#post':
    #             posts.append(item)
    
    titles = []
            
    posts = get_posts(children)
                    
    images = []

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

        
        root2 = get_post_html(post)
        children2=get_children(root2)
        my_images = []
        for item in children2:
            try:
                tag = item.tag
                if tag.lower()=='img':
                    my_images.append((item,title))
            except AttributeError:
                pass
        images.extend(my_images)

    titles_clean = [cleantext(item) for item in titles]
    
    srcs = [(item.attrib['src'],title) for item,title in images]    
    src_dictionary = {}

    for key,page in srcs:
        src_dictionary[key]={'pages':[]}
        
    for key,page in srcs:
        src_dictionary[key]['pages'].append(page)

    for key in src_dictionary.keys():
        src_dictionary[key]['pages'] = list(set(src_dictionary[key]['pages']))

    ii=0
    for key in src_dictionary.keys():
        ftype = os.path.splitext(key)[1].lower()
        src_dictionary[key]['filename']='figure_{0:03.0f}{1:s}'.format(ii,ftype)
        ii+=1
        
    
    if os.path.exists(export_folder):
        shutil.rmtree(export_folder)
    time.sleep(1)
    os.mkdir(export_folder)
    os.mkdir(image_folder)
    
    errors = []
    
    for key in src_dictionary.keys():
        try:
            r = requests.get(key) # create HTTP response object 
            if r.ok:
                with open(os.path.join(image_folder,src_dictionary[key]['filename']),'wb') as f: 
                    f.write(r.content)     
                img = PIL.Image.open(os.path.join(image_folder,src_dictionary[key]['filename']))
                itype = imtypemapping[img.format.lower()]
                del img
                froot,ctype = os.path.splitext(src_dictionary[key]['filename'])
                new = froot+'.'+itype.lower()
                os.rename(os.path.join(image_folder,src_dictionary[key]['filename']),os.path.join(image_folder,froot+'.'+itype.lower()))
                src_dictionary[key]['filename'] = new
            else:
                errors.append(('404',key,src_dictionary[key]))
        except requests.exceptions.InvalidSchema as e:
            errors.append((e,key,src_dictionary[key]))
            
    
    # mapping_fwd = dict([tuple(item) for item in mapping])
        
    for post,title in zip(posts,titles):
        item = post.find('{http://www.w3.org/2005/Atom}content')
        text = item.text
        textb = text.encode('utf-8')
        root2 = et.HTML(textb)
        children2=get_children(root2)
        for item2 in children2:
            try:
                tag = item2.tag
                if tag.lower()=='img':
                    item2.attrib['src']='figures/'+src_dictionary[item2.attrib['src']]['filename']
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
        
    page_info_mapping = []
    
    for p,filename,title in zip(posts,titles_clean,titles):
        categories = get_categories(p)
        page_info = {}
        page_info['title'] = title
        page_info['tags'] = categories
        page_info_mapping.append((filename,page_info))
    
    page_info_mapping = dict(page_info_mapping)
    
    with open(os.path.join(root_path,'page_info.yaml'),'w') as f:
        yaml.dump(page_info_mapping,f)
        
        