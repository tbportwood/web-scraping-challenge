from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from splinter import Browser

def scrape_all():
    
    from bs4 import BeautifulSoup as bs
    import pandas as pd
    import requests
    from splinter import Browser

    #news scraping
    url = 'https://mars.nasa.gov/news/'
    executable_path = {'executable_path': 'Missions_to_Mars\chromedriver.exe'}
    browser = Browser('chrome', **executable_path)
    browser.visit(url)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=10)
    mars_soup = bs(browser.html, 'html.parser')
    news_p = mars_soup.find_all('li', class_ = 'slide')[0].a.div.text
    news_title = mars_soup.find_all('li', class_ = 'slide')[0].a.h3.text

    #featured image scraping
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    featured_image_url = soup.find('article', class_='carousel_item')
    featured_image_url = featured_image_url["style"]
    import re
    featured_image_url = re.findall("url\(\'/(.+?)\'\)", featured_image_url)
    featured_image_url = 'https://www.jpl.nasa.gov/' + featured_image_url[0]

    #weather tweet scraping
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    browser.is_element_present_by_tag("article", wait_time=10)
    html = browser.html
    soup = bs(html, 'html.parser')
    mars_weather_span = soup.article.find_all('span')
    print(mars_weather_span)
    tweet_text = mars_weather_span[4].text
    mars_weather = tweet_text
    mars_weather

    #mars facts
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    html = browser.html
    tables = pd.read_html(html)
    tables[0] = tables[0].rename(columns = {0:"", 1:"Values"})
    tables[0] = tables[0].set_index("")
    mars_facts = tables[0].to_html()

    #mars hemisphere urls
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    hemisphere_soup = bs(html, 'html.parser')
    hem_soup_urls = hemisphere_soup.find_all('div', class_='item')
    urls = []
    for item in range(0,4):
        urls.append('https://astrogeology.usgs.gov' + hem_soup_urls[item].a['href'])
    hemisphere_image_urls = []
    for i in range(0,4):
        browser.visit(urls[i])
        html = browser.html
        images_urls = bs(html, 'html.parser')
        image_url = images_urls.find_all('li')[0].a['href']
        images_urls.title.text
        title = re.findall("(.+?) Enhanced", images_urls.title.text)[0]
        hemisphere_image_urls.append({'title': title, 'img_url': image_url })

    mars_data =  {'hemisphere_image_urls': hemisphere_image_urls, \
                'mars_weather': mars_weather, \
                'featured_image_url': featured_image_url, \
                'mars_facts': mars_facts, \
                'news_title': news_title, \
                'news_p': news_p}
    browser.quit()

    return mars_data