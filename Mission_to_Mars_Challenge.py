# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import re

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

url = 'https://marshemispheres.com/'
browser.visit(url)

html = browser.html
soup = soup(html, "html.parser")

img_url_rel=soup.select("div.item [href]")

urls_all = [link['href'] for link in img_url_rel]
urls_all

urls = pd.unique(urls_all).tolist()
urls

image_url = []

for i in urls:
      image_url.append(f'https://marshemispheres.com/{i}')
        
print(image_url)

ttls = soup.find_all('h3')
image_title = []

for titles in ttls:
    image_title.append(titles.text)  

image_title.remove('Back')
print(image_title)


# The only was to get the next part of the code to work was
# to reimport all the dependencies

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import re

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

full_images = []

for url in image_url:
    browser.visit(url)
    html = browser.html

    image_soup = soup(html, "html.parser")

    sample_images = image_soup.find('a',href=True,text='Sample').get('href')
    
    full_images.append(sample_images)

browser.back()

full_images_urls = []

for x in full_images:
    x1 = f'https://marshemispheres.com/{x}'
    full_images_urls.append(x1)
    
hemisphere_image_urls = []

for x in range(len(full_images_urls)):
    hemisphere = {
        "img_url": full_images_urls[x],
        "title": image_title[x]
    }
    hemisphere_image_urls.append(hemisphere)
       
hemisphere_image_urls

browser.quit()

