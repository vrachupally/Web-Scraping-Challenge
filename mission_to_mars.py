#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
from flask import Flask, render_template, redirect
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ## NASA Mars News

# In[3]:


url = "https://mars.nasa.gov/news"
browser.visit(url)

html = browser.html

news_soup = bs(html, 'html.parser')
# news_soup


# In[4]:


news = news_soup.select_one('ul.item_list li.slide')
news


# In[5]:


title = news.find_all('div', class_='content_title')
news_title = title[0].text.strip()
news_title


# In[6]:


para = news.find_all('div', class_='article_teaser_body')
news_p = para[0].text.strip()
news_p


# ## JPL Mars Space Images - Featured Image

# In[7]:


url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)


# In[8]:


html = browser.html

image_soup = bs(html, 'html.parser')
# image_soup


# In[9]:


images = image_soup.find_all('div', class_='floating_text_area')
images


# In[10]:


for img in images:
    link = img.find('a')
    href = link['href']
    print( 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + href )
featured_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + href


# ## Mars Facts

# In[11]:


df = pd.read_html('https://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df


# In[12]:


df.to_html()


# ## Mars Hemispheres

# In[13]:


url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[14]:


hemisphere_image_urls = []
links = browser.find_by_css("a.product-item h3")

for i in range(len(links)):
    hemisphere = {}
    
    browser.find_by_css("a.product-item h3")[i].click()

    sample_elem = browser.links.find_by_text('Sample').first
    hemisphere['img_url'] = sample_elem['href']

    hemisphere['title'] = browser.find_by_css("h2.title").text

    hemisphere_image_urls.append(hemisphere)

    browser.back()


# In[15]:


hemisphere_image_urls
