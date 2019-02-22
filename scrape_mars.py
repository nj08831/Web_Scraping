# Source: My work.  
#IMPORTS
from bs4 import BeautifulSoup
import requests
import os
import io
from splinter import Browser

import pandas as pd
from zipfile import ZipFile

def scrape():
    # URL of page to be scraped
    url = "https://mars.nasa.gov/news/"

    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')
    soup
    # Retrieve the first article on NASA Site
    article_title = soup.find_all('div', class_='content_title')
    the_title = article_title[0].text

    the_title = the_title.strip('\n')
    the_title

    # Retrieve the first article Text
    article = soup.find_all('div', class_='rollover_description_inner')
    article = article[0].text

    the_article = article.strip('\n')
    the_article

   
    # Scrape the MARS Site
    executable_path = {'executable_path': 'c:/users/pa223/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find the URL HTTP Link to 2nd page to grab the large image
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # I found on website how to do the 'get' function.  
    button = soup.find_all('a', class_='button fancybox')[0].get('data-link').strip()
    button

    # Combine the URL to make the HTML page
    html_page = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars' + button

    browser.visit(html_page)
    html_page

    # Identify the large Image in the image box section
    featured_image_url = soup.find_all('a', class_='fancybox')[1].get('data-fancybox-href')
    featured_image_url
    
    short_url = "https://www.jpl.nasa.gov"
    featured_image_url = short_url + featured_image_url
    featured_image_url

    # TWITTER SCRAPE
    # URL of page to be scraped
    twitter_url = "https://twitter.com/marswxreport"

    # Retrieve page with the requests module
    response = requests.get(twitter_url)

    # Create BeautifulSoup object; parse with 'lxml'
    twitter_soup = BeautifulSoup(response.text, 'lxml')

    twitter_soup

    # Retrieve the Weather from Twitter 

    tweet = twitter_soup.find_all('div', class_='js-tweet-text-container')

    # find the weather, starts with Sol
    for p in tweet:
        x = p.text
        if x.strip()[:3] == 'Sol':
            weather = p.text
   
            break

    #strip the \n from the data
    weather_tweet = weather.strip('\n')
    weather_tweet

    # identify the end of the string - there is extraneous text
    mars = weather_tweet.find('pic')
    print(f' {mars} is the end of the string for weather')
    print('')
    mars_weather = weather_tweet[:mars]

    mars_weather

    # Scraping and finding the Mars Facts
    url = 'https://space-facts.com/mars/'

    
    dfs = pd.read_html(url)
    dfs
    df = dfs[0]
    df
    df.columns = ['Mars_Fact_Description', 'Mars_Value']
    df

    executable_path = {'executable_path': 'c:/users/pa223/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Find the URL HTTP Link to 2nd page to grab the large image
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # I found on website how to do the 'get' function.  
    buttons = soup.find_all('a', class_='itemLink product-item')#[0].get('href').strip()
    buttons

    # Pull each of the URLs needed to grab the main Mars image
    urls = []
    x=0
    for button in buttons:
        urls.append(soup.find_all('a', class_='itemLink product-item')[x].get('href').strip())
        x=x+1

    urls
    # deduping the list
    urls = list(dict.fromkeys(urls))
    urls

    #Doing a For loop to goto each Web page and grab the correct main image

    image_url = 'https://astrogeology.usgs.gov/'

    image = []
    title = []

    print('')
    print('Printing each website page , the URL of the main image, and the title')
    print('')
    for url in urls:
        button = url
        click_button = image_url + button
        print(click_button)

        browser.visit(click_button)
        html1 = browser.html
        soup = BeautifulSoup(html1, 'html.parser')
        main_image = soup.find_all('img', class_='wide-image')[0].get('src').strip()
        print(main_image)
        main_title =soup.find('h2', class_='title').text
        print(main_title)
        image.append(image_url + main_image)
        title.append(main_title)

    #MY FINAL DICTIONARY AND THE STEPS

    # Make a dictionary
    # start with the NASA Site Scrape
    my_final_dict = {"nasa_title" : the_title , "nasa_article": the_article}
    my_final_dict

    # From MARS Site Scrape
    mars_site = {"mars_featured_image" : featured_image_url}

    my_final_dict.update(mars_site)
    my_final_dict

    # From Twitter Site Scrape
    mars_twitter = {"mars_weather" : mars_weather}

    my_final_dict.update(mars_twitter)
    my_final_dict

    # From Mars Site
    # Convert dataframe to dictionary
    # mars = df.to_dict()

    #my_final_dict.update(mars)
    #my_final_dict

    # From Astropedia Site 
    #create a dictionary of the images and titles

    dict_images = list(zip(image,title))
    df_images = pd.DataFrame(dict_images, columns = ['image_url', 'title'])
    df_images.reset_index(drop=True, inplace=True)
    new_dict = {"atitle" : list(df_images['title']), "aimage_url" : list(df_images['image_url'])}
    new_dict

    my_final_dict.update(new_dict)
    my_final_dict
    print(my_final_dict)
    return my_final_dict



