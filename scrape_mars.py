# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests


def start_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = start_browser()
    mars_list = {}


    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Extract title and paragraph text.
    news_title = browser.find_by_css("div.content_title a").text
    news_p = browser.find_by_css("div.article_teaser_body").text

    # Display Data
    print(news_title)
    print(news_p)

    # Visit visit url
    url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # src of image
    image_path = soup.find('img', class_='headerimage fade-in')['src']
    image_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/"
    mars_space_img = image_url + image_path

    # print results
    print(mars_space_img)

    # URL for Mars Facts
    mars_facts_url = "https://space-facts.com/mars"

    # Scrape Mars Facts Table
    mars_facts_table = pd.read_html(mars_facts_url)

    # Mars Facts Table
    mars_facts_df = mars_facts_table[0]
    mars_facts_df.columns = ["Description","Mars"]
    mars_facts_df.set_index("Description", inplace=True)
    mars_facts_df.to_html()
    data = mars_facts_df.to_html('mars_facts_df.html') 
    mars_facts_df

    # URL of page to be scraped
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)

    # Retrieve page with the requests module
    html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(html, 'html.parser')

    hemisphere_images = []


    for results in soup.find_all('div', class_='accordian'):    
        for list in soup.find_all('div', class_='item'):
            title_img_dict = {}
            url = 'https://astrogeology.usgs.gov/' + list.a.get('href')
            response = requests.get(url)
            soup = bs(response.text, 'html.parser')
            title = soup.find('h2', class_='title')
            title_img_dict["title"] = title.text
            image = soup.find('div', class_='downloads')
            title_img_dict["img_url"] = image.a['href']
            hemisphere_images.append(title_img_dict)
            
    print(hemisphere_images)