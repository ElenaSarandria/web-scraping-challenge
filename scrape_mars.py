#import dependencies
from bs4 import BeautifulSoup as bs
import requests
import pymongo
import time
import pandas as pd
from splinter import Browser

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

mars_info = {}

def scrape_mars_news():
    try:
        browser = init_browser()
        
        # Visit the NASA website
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)
        time.sleep(1)
    
        # Scrape page into Soup
        html = browser.html
        soup1 = bs(html, 'html.parser')
        time.sleep(1)
        #Find the latest news title and headline text in the beautiful soup
        news_title = soup1.find('div', class_='content_title').text
        time.sleep(1)
        news_p = soup1.find('div', class_='article_teaser_body').text
        time.sleep(1)
        print(f'The latest news title: {news_title}')
        print(f'News paragraph: {news_p}')
    
        mars_info['news_title'] = news_title
        mars_info['news_paragraph'] = news_p
        
        print("Mars News")
        print(mars_info)
    
        return mars_info
    finally:
        browser.quit()
    
    # JPL url to scrape featured images
def scrape_mars_image():
    try:
        browser = init_browser()
        
        images_url = 'http://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(images_url)
        time.sleep(1)
        html_images = browser.html
    
        # Create a Beautiful Soup object
        soup2 = bs(html_images, 'html.parser')
        time.sleep(1)
        #Find the image in soup
        search_image_url = soup2.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
        main_url = 'http://www.jpl.nasa.gov'
        
        search_image_url = main_url+search_image_url
        search_image_url
    
        mars_info['search_image_url'] = search_image_url
    
        return mars_info
    finally:
        browser.quit()

    #Visit Mars Weather Twitter
def scrape_mars_weather():
    try:
        browser = init_browser()
        weather_twitter_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(weather_twitter_url)
        time.sleep(3)
        html_twitter = browser.html
    
        # Create a Beautiful Soup object
        soup3 = bs(html_twitter, 'html.parser')
        time.sleep(1)
        #Find the text in soup
        
        #none of these methods(showed below) didn't work. I'm assume because in my jupyter notebook my code shoded me as a result "log in", the same problem is when python is trying to run twitter page it's trying to log in nd failed every time. I don't have other explanation why it tris to run twitter and failed every time
        
        #This is the class which I got from twiiter <span class="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0">InSight sol 457 (2020-03-10) low -95.7ºC (-140.3ºF) high -9.1ºC (15.6ºF) winds from the SSE at 6.5 m/s (14.5 mph) gusting to 21.0 m/s (46.9 mph)pressure at 6.30 hPa</span>
        
        #mars_weather_twitter = soup.find('p', {'class': 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text'})
        mars_weather_twitter = soup3.find('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0').text
        #mars_weather_twitter = soup3.find('div',class_='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0').text
        
        #latest_twitter = soup3.find_all('div', class_='js-tweet-text-container')
        #for tweet in latest_twitter:
            #mars_weather_twitter = tweet.find('p').text
            #if 'sol' and 'SSE' in mars_weather_twitter:
                #print(mars_weather_twitter)
                #break
            #else:
                #pass
                
        mars_info['mars_weather_twitter'] = mars_weather_twitter
        
    
        return mars_info
    finally:
        browser.quit()
    
    #Visit the Mars facts webpage
def scrape_mars_facts():
    try:
        browser = init_browser()
    
        mars_facts_url = 'https://space-facts.com/mars/'
        browser.visit(mars_facts_url)
        time.sleep(1)
        html_facts = browser.html
        soup4 = bs(html_facts, 'html.parser')
        time.sleep(1)

        #Find the text in soup
        mars_table =  soup4.find('table', class_='tablepress tablepress-id-p-mars')
        c1 = mars_table.find_all('td', class_='column-1')
        c2 = mars_table.find_all('td', class_='column-2')
        mars = []
        value_mars = []
        for i in c1:
            mars.append(i.text.strip())
        for j in c2:
            value_mars.append(j.text.strip())
        mars_facts_pd = pd.DataFrame({
            'Description': mars,
            'Value': value_mars
            })
        
        # convert dataframe to html
        html_table = mars_facts_pd.to_html(header=False, index=False)
        
        #read_html(mars_facts_url)
        #mars_df = mars_facts_pd[0]
        #Create df
        #mars_df.columns = ['Description', 'Value']
        #mars_df.set_index('Description', inplace=True)
        #html_table = mars_df.to_html()
    
        mars_info['mars_facts_pd'] = html_table
    
        return mars_info
    finally:
        browser.quit()
    
    #Visit the Mars USGS Astrogeology site
def scrape_mars_hemispheres():
    try:
        browser = init_browser()
    
        mars_hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(mars_hemisphere_url)
        time.sleep(1)
        html_hemisphere = browser.html
    
        # Create a Beautiful Soup object
        soup5 = bs(html_hemisphere, 'html.parser')
        time.sleep(1)
        items = soup5.find_all('div', class_='item')
        hemisphere_image_url = []
        mars_hemisphere_main_url = 'https://astrogeology.usgs.gov'
        # Loop over results to get image urls
        for i in items:
            title = i.find('h3').text
            image_url = i.find('a', class_='itemLink product-item')['href']
            browser.visit(mars_hemisphere_main_url + image_url)
            image_html = browser.html
        
            soup5 = bs(image_html, 'html.parser')
            img_url = mars_hemisphere_main_url + soup5.find('img', class_='wide-image')['src']
            hemisphere_image_url.append({"title": title, "img_url": img_url})
        
        
    # Store data in a dictionary
    #mars_info = {
        #"news_title": news_title,
        #"news_p": news_p,
        #"search_image_url": search_image_url,
        #"mars_weather_twitt": mars_weather_twitt,
        #"html_table": html_table,
        #"hemisphere_image_url": hemisphere_image_url
#}
    
        mars_info['hemisphere_image_url'] = hemisphere_image_url
    
        # Return results
        return mars_info
            
        # Close the browser after scraping
    finally:
        browser.quit()

