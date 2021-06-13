
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import numpy as np
import lxml

def scrape():
    
    # browser = init_browser()
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # NASA Mars News
    url = "https://redplanetscience.com/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    news_title_all = soup.body.find_all("div", class_="content_title")
    news_p_all = soup.body.find_all("div", class_="article_teaser_body")

    news_title = news_title_all[0].get_text()
    news_title

    news_p = news_p_all[0].get_text()
    news_p

    # JPL Mars Space Images - Featured Image
    mars_img_url = "https://spaceimages-mars.com/"
    browser.visit(mars_img_url)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    head_image = soup.body.find("img", class_="headerimage")
    head_img_src = head_image['src']

    featured_image_url = f'https://spaceimages-mars.com/{head_img_src}'
    

    # Mars Facts
    mars_data_url = "https://galaxyfacts-mars.com/"
    browser.visit(mars_data_url)
    time.sleep(1)

    html = browser.html

    table = pd.read_html(html)

    mars_facts_df = table[0]
    mars_facts_df.columns = ['Description', 'Mars', 'Earth']
    mars_facts_df.reset_index(drop=True)
    mars_facts_html = mars_facts_df.to_html(index = False, header = False, border=0)

    # Mars Hemispheres

    mars_image_url = "https://marshemispheres.com/"
    browser.visit(mars_image_url)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    hemi_t = soup.body.find_all("h3")
    hemi_title = []
    for i in range(len(hemi_t)):
        if hemi_t[i].text != 'Back':
            hemi_title.append(hemi_t[i].text)
            i =i+1

    hemi_imgs = []
    hrefs = soup.body.find_all("a", class_="itemLink product-item")
    for hemi in hrefs:
        hemi_imgs.append(hemi['href'])

    hemi_img_html = []
    for i in range(len(hemi_imgs)-1):
        if (hemi_imgs[i] != hemi_imgs[i+1]) and (hemi_imgs[i] != '#'):
            hemi_img_html.append(hemi_imgs[i])
            i =i+1
    if hemi_imgs[len(hemi_imgs)-1] != '#':
        hemi_img_html.append(hemi_imgs[len(hemi_imgs)-1])

    hemi_full_img = []
    for i in range(len(hemi_img_html)):
        img_html = hemi_img_html[i]
        hemi_full_img_url = f'https://marshemispheres.com/{img_html}'
        browser.visit(hemi_full_img_url)
        time.sleep(1)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        full_img_find = soup.body.find("img", class_="wide-image")
        full_img_src = full_img_find["src"]
        hemi_full_img.append(full_img_src)

    hemi_url = []
    for i in range(len(hemi_title)):
        img_title = hemi_title[i]
        full_hemi_img_url = hemi_full_img[i]
        hemi_url.append({"title":img_title, "img_url":f'https://marshemispheres.com/{full_hemi_img_url}'})

    listings_data = {"news_title": news_title,
    "news_content": news_p,
    "mars_featured_img": featured_image_url,
    "mars_facts_html": mars_facts_html,
    "hemisphere_images": hemi_url}


    # Quit the browser
    browser.quit()
   
    return listings_data
