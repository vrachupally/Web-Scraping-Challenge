from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from webdriver_manager.chrome import ChromeDriverManager

data = {}


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    mars_news(browser)
    featured_image(browser)
    mars_facts()
    hemispheres(browser)

    browser.quit()

    return data


# NASA Mars News
def mars_news(browser):
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    news_soup = bs(html, "html.parser")

    try:
        news = news_soup.select_one("ul.item_list li.slide")
        news_title = news.find("div", class_="content_title").get_text()
        news_p = news.find(
            "div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    data["news_title"] = news_title
    data["news_paragraph"] = news_p

    return


# JPL Mars Space Images - Featured Image
def featured_image(browser):
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    html = browser.html
    image_soup = bs(html, 'html.parser')

    try:
        image = image_soup.select_one('div.floating_text_area')
        href = image.find('a', class_='showimg fancybox-thumbs').get("href")

    except AttributeError:
        return None

    featured_image_url = 'https://spaceimages-mars.com/' + href
    data["featured_image"] = featured_image_url

    return


# Mars Facts
def mars_facts():
    try:
        df = pd.read_html("http://space-facts.com/mars/")[0]
    except BaseException:
        return None

    df.columns = ["description", "value"]
    data["facts"] = df.to_html(index=False)

    return


# Mars Hemispheres
def hemispheres(browser):
    url = (
        "https://astrogeology.usgs.gov/search/"
        "results?q=hemisphere+enhanced&k1=target&v1=Mars"
    )

    browser.visit(url)
    browser.is_element_present_by_text(
        "USGS Astrogeology Science Center", wait_time=1)

    hemisphere_image_urls = []

    for i in range(4):
        hemisphere = {}

        browser.find_by_css("a.product-item h3")[i].click()

        html = browser.html
        hemi_soup = bs(html, "html.parser")

        hemisphere['title'] = hemi_soup.find("h2", class_="title").get_text()
        hemisphere['img_url'] = hemi_soup.find("a", text="Sample").get("href")

        hemisphere_image_urls.append(hemisphere)

        browser.back()

    data["hemispheres"] = hemisphere_image_urls

    return


if __name__ == "__main__":

    # If running as script, print scraped data
    print()
