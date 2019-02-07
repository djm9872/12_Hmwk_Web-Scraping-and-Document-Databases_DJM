
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import pymongo
import pandas as pd
from pprint import pprint
import time
import re




def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)




def scrape_info():
    browser = init_browser()

    #Create master dictionary to hold all the variables
    scrape_dict = {}

#_______________________________________________________________
    # ### Nasa Mars News Scrape

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    time.sleep(1)
    html = browser.html


    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(html, 'html.parser')

    #Grab the Title and teaser paragraph for first article on the website
    title_results = soup.find_all('li', class_='slide')

    #Create list variables to store
    titles = []
    news_p = []

    #Loop through the title_results tags to identify the title and teaser body and append to respective lists above
    for items in title_results:
        news_title = items.find('div', class_= 'content_title').a.text
        titles.append(news_title)
        
        news_teaser = items.find('div', class_='article_teaser_body').text
        news_p.append(news_teaser)

    #Print first item in each list to verify
    # print(titles[0])
    # print(news_p[0])

    #Set news_title and news_teaser variables with the first item in each list respectively
    scrape_dict['news_title'] = titles[0]
    scrape_dict ['news_teaser'] = news_p[0]

#_______________________________________________________________
    # ### JPL Mars Space - Featured Image Scrape

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(1)
    html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(html, 'html.parser')

    #Find the article tag with class carousel item
    img_results = soup.find_all('article', class_='carousel_item')

    #Within the article tag pull out the text that is in the "style" tag
    img = img_results[0]['style']

    #Separate the string to only the url image
    img_string = re.findall("'.*'", img_results[0]['style'])[0].replace("'","")

    #Set variable with main url
    main_url = 'https://www.jpl.nasa.gov'

    #Concatenate the full url for the image
    scrape_dict['featured_image_url'] = main_url + img_string

    #Print out string to verify
    # print(featured_image_url)

#_______________________________________________________________
    # ### Mars Weather Scrape

    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(1)
    html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(html, 'html.parser')

    #Identify the html code that contains the tweets
    tweet_results = soup.find_all('div', class_='js-tweet-text-container')

    tweets = []

    #Loop through all the tweets and pull out the tweet paragraph and append to tweets list
    for tweet in tweet_results:
        new_tweets = tweet.find('p').text
        tweets.append(new_tweets)

    #Print first item in tweets list to verify it's pulling the first tweet    
    # print(tweets[0])

    #Set mars_weather variable with first item in tweets list
    scrape_dict['mars_weather'] = tweets[0]


#_______________________________________________________________
    # ### Mars Facts Scrape

    url = 'https://space-facts.com/mars/'

    #Read the url with pandas to find the table
    tables = pd.read_html(url)
    print(tables)

    #Create a dataframe with the first table
    table_df = tables[0]

    #Rename the dataframe columns
    table_df.columns = ['description', 'fact']

    #Verify dataframe
    # table_df.head()

    #Convert the dataframe back to html string 
    scrape_dict['table'] = table_df.to_html()


#_______________________________________________________________
    # ### Mars Hemispheres Scrape

    #Set list and dictionaries to store scraped data
    hemisphere_image_urls = []
    image_dict1 = {}
    image_dict2 = {}
    image_dict3 = {}
    image_dict4 = {}

    #Go to desired url and click on the required page link to get the first image
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(2)
    browser.click_link_by_partial_text('Cerberus Hemisphere Enhanced')
    html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(html, 'html.parser')

    #Identify the html tag for the needed information
    container = soup.find('div', class_='container')

    #Find the title of the desired image and append to a dictionary
    name = container.find('h2', class_='title').text
    image_dict1['title'] = name

    #Find the image url and append to the dictionary
    image = container.find('div', class_='downloads').li.a['href']
    image_dict1['img_url'] = image

    #Append the dictionary to the list
    hemisphere_image_urls.append(image_dict1)

    #Go back one page in the browser and then click into the next page
    browser.click_link_by_partial_text('Back')
    time.sleep(1)
    browser.click_link_by_partial_text('Schiaparelli Hemisphere Enhanced')

    #Repeat steps above three more times to get all the titles and images
    html = browser.html
    soup = bs(html, 'html.parser')

    container = soup.find('div', class_='container')

    name = container.find('h2', class_='title').text
    image_dict2['title'] = name

    image = container.find('div', class_='downloads').li.a['href']
    image_dict2['img_url'] = image

    hemisphere_image_urls.append(image_dict2)


    browser.click_link_by_partial_text('Back')
    time.sleep(1)
    browser.click_link_by_partial_text('Syrtis Major Hemisphere Enhanced')

    html = browser.html
    soup = bs(html, 'html.parser')

    container = soup.find('div', class_='container')

    name = container.find('h2', class_='title').text
    image_dict3['title'] = name

    image = container.find('div', class_='downloads').li.a['href']
    image_dict3['img_url'] = image

    hemisphere_image_urls.append(image_dict3)

    browser.click_link_by_partial_text('Back')
    time.sleep(1)
    browser.click_link_by_partial_text('Valles Marineris Hemisphere Enhanced')

    html = browser.html
    soup = bs(html, 'html.parser')

    container = soup.find('div', class_='container')

    name = container.find('h2', class_='title').text
    image_dict4['title'] = name

    image = container.find('div', class_='downloads').li.a['href']
    image_dict4['img_url'] = image

    hemisphere_image_urls.append(image_dict4)

    scrape_dict['hemisphere_image_urls'] = hemisphere_image_urls

    browser.quit()

    return scrape_dict

    #Print hemispere_image_urls to verify and print scrape_dict to make sure everything is in the master dictionary
    # print(hemisphere_image_urls)
    #print(scrape_dict)



      

