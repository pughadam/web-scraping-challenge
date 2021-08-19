# Import Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests
import pymongo



def scrape_all():
    # Set a path and initialize Chrome Browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_t, news_p = mars_news(browser)
    featured_img = featured_image(browser)
    mars_data = mars_facts(browser)
    hemisphere_image_url = hemisphere(browser)

    mars = {
        "news_title": news_t,
        "news_paragraph": news_p,
        "featured_image": featured_img,
        "mars_table": mars_data,
        "hemisphere_image_url": hemisphere_image_url
    }
    browser.quit()

    return mars

def mars_news(browser):
    # Visit the website
    url = 'https://redplanetscience.com/'
    browser.visit(url)


    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find("div",class_="content_title").text
    news_paragraph = soup.find("div", class_="article_teaser_body").text
    # print(f"Title: {news_title}")
    # print(f"Para: {news_paragraph}"

    return news_title, news_paragraph


def featured_image(browser):
# # JPL Mars Space Images - Featured Image
    # url_image = 'https://spaceimages-mars.com/image/featured/mars2.jpg'
    # browser.visit(url_image)
    browser.visit('https://spaceimages-mars.com/')
    browser.click_link_by_partial_text('FULL IMAGE')

    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    mars_space_image_soup = BeautifulSoup(html, 'html.parser')

    mars_image = mars_space_image_soup.find("img",class_="fancybox-image")['src']
    # print(mars_image)

    full_image_url = 'https://spaceimages-mars.com/' + mars_image

    return full_image_url


def mars_facts(browser):
    # # Mars Facts
    # url = 'https://galaxyfacts-mars.com'
    # Read in data from the website provided

    mars_table = pd.read_html('https://galaxyfacts-mars.com')[0]
    # Print table to make sure I'm pulling the right infomration
    # print(mars_table)

    # Reset the dataframe with the correct titles
    mars_table.columns=["Properties", "Mars", "Earth"]
    mars_table.set_index("Properties", inplace=True)
    mars_table

    mars_table.to_html()

    # mars_table = mars_table.to_html()

    # return mars_table
    return mars_table.to_html()

def hemisphere(browser):
    # # Mars Hemispheres
    # Set a path and initialize Chrome Browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit the website
    url = url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Make an empty list to loop through for the images
    hemisphere_image_url = []
    # Add the link for the css/html for reference
    links = browser.find_by_css("a.product-item img")

    # create a loop to get the image url's
    for item in range(len(links)):
        hemisphere = {}
        
        # find each element
        browser.find_by_css("a.product-item img")[item].click()
        
        # finding sample image and href
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]
        
        # get the title of the Mars hemisphere
        hemisphere["title"] = browser.find_by_css("h2.title").text
        
        # append to list
        hemisphere_image_url.append(hemisphere)
        
        # 
        browser.back()

        # get the images and urls
    return hemisphere_image_url




