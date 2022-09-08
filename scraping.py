#!/usr/bin/env python
# coding: utf-8

from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd 
import datetime as dt

def scrape_all():
        # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    news_title, news_paragraph = mars_news(browser)
        # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemisphere_image_urls": hemisphere_list(browser)
                }   
    browser.quit()
    return data

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

        # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

        # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
        
        # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
            
            return None, None
    return news_title, news_p

    # ### Featured Images
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)


        # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

        # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
        # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    except AttributeError:
            return None
        # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url
    # ## Mars Facts
def mars_facts():
            # Add try/except for error handling
    try:
            # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    return df.to_html(classes="table table-striped")

def hemisphere_list(browser):
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com'

    browser.visit(url)
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []
    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    html = browser.html
    img_soup = soup(html, 'html.parser')  

    all_images = img_soup.find('div', class_='collapsible results')

    image_link = all_images.find_all('div',class_='item')

    for imagelink in image_link:
        
        title = imagelink.find('div', class_ = 'description')
        title1 = title.find('h3').text
        #hemisphere_image_title.append(title)
        book_url = imagelink.find('a')['href']
        browser.visit('https://marshemispheres.com/' + book_url)
        img1 = browser.html
        link = soup(img1,'html.parser')
        link1 = link.find('div', class_='downloads')
        link2 = link1.find('a').get('href')
        link3 = ('https://marshemispheres.com/' + link2)
        Dict = {'title': title1, 'img_url': link3}
        hemisphere_image_urls.append(Dict)
    return hemisphere_image_urls

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())