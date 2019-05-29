from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import time
import pandas as pd

def init_browser():
    return Browser("chrome", executable_path="chromedriver", headless=False)

def scrape():
    browser = init_browser()
    mars_facts_data = {}

    news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    response = requests.get(news_url)
    

    soup = bs(response.text, "html.parser")

    #scrapping latest news about mars from nasa
    title = soup.find("div",class_="content_title").text
    news_p = soup.find("div",class_="rollover_description_inner").text
    mars_facts_data['news_title'] = title
    mars_facts_data['news_paragraph'] = news_p 
    
    #Mars Featured Image
    JPL_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(JPL_url)
    time.sleep(15)
    html = browser.html
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(10)
    browser.click_link_by_partial_text('more info')
    image_html = browser.html
    new_soup = bs(image_html, 'html.parser')
    container = new_soup.find('img', class_='main_image')
    src_url = container.get('src')

    featured_image_url  = "https://www.jpl.nasa.gov/" + src_url
    mars_facts_data["featured_image"] = featured_image_url

#Mars Weather
    twitter_url ="https://twitter.com/marswxreport?lang=en"
    response = requests.get(twitter_url)
    weather_soup = bs(response.text, 'html.parser')
    tweet_container = weather_soup.find('div', class_="js-tweet-text-container")
    mars_weather = tweet_container.text
    mars_facts_data["mars_weather"] = mars_weather

# #### Mars Facts
    facts_url = "https://space-facts.com/mars/"
    time.sleep(2)
    facts_response = requests.get(facts_url)
    mars_facts_tb = pd.read_html(facts_response.text)
    df_mars_facts = mars_facts_tb[0]


    df_mars_facts.columns = ["Parameter", "Values"]
    clean_table = df_mars_facts.set_index(["Parameter"])
    mars_html_table = clean_table.to_html()
    mars_html_table = mars_html_table.replace("\n", "")
    mars_facts_data["mars_facts_table"] = mars_html_table

    #save table to HTML
    df_mars_facts.to_html('mars_table.html', index=False)


# #### Mars Hemisperes

    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    hemi_response = requests.get(hemi_url)

    soup = bs(hemi_response.text, "html.parser")
    hemi_container = soup.find_all('div', class_="item")
    hemisphere_img_urls = []

    for i in hemi_container:
    	title = i.find('h3').text                                        #Get title
    	url_container = i.find('a')
    	url = url_container['href']
    	img_url = "https://astrogeology.usgs.gov/" + url           #get image link
    	img_request = requests.get(img_url)                        #start new request to get full image
    	soup = bs(img_request.text, 'html.parser')
    	img_tag = soup.find('div', class_='downloads')
    	img_url2 = img_tag.find('a')['href']
    	hemisphere_img_urls.append({"Title": title, "Image_Url": img_url2})


    mars_facts_data["hemisphere_img_url"] = hemisphere_img_urls

    browser.quit()
    print(mars_facts_data)
    return mars_facts_data

