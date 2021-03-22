from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
from flask import Flask, render_template, redirect
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_dict = {}


### NASA Mars News
url = "https://mars.nasa.gov/news"
browser.visit(url)
html = browser.html
news_soup = bs(html, 'html.parser')
# news_soup

news = news_soup.select_one('ul.item_list li.slide')
news

title = news.find_all('div', class_='content_title')
news_title = title[0].text.strip()
news_title

para = news.find_all('div', class_='article_teaser_body')
news_p = para[0].text.strip()
news_p


### JPL Mars Space Images - Featured Image

url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)
html = browser.html
image_soup = bs(html, 'html.parser')
# image_soup

images = image_soup.find_all('div', class_='floating_text_area')
images

for img in images:
    link = img.find('a')
    href = link['href']
    print( 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + href )
featured_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + href


### Mars Facts

df = pd.read_html('https://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df

fact_table = df.to_html()
fact_table

### Mars Hemispheres

url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)

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

hemisphere_image_urls

mars_dict={
        "News Title":news_title,
        "News Paragraph Text":news_p,
        "Featured Image Url":featured_image_url,
        "Facts Table":fact_table,
        "Hemisphere Images":hemisphere_image_urls}