# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "last_modified": dt.datetime.now(),
      "hemispheres": hemi_data(browser)
        }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    # url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:
        slide_elem = news_soup.select_one('div.list_text')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None

    return news_title, news_p

# ### JPL Featured Images
def featured_image(browser):
# Visit URL
    url = 'https://spaceimages-mars.com'
# url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
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
    
    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    # img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

# ## Mars facts

def mars_facts():
    # Add try/except for error handling
    try:
      # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
        # df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # return df.to_html()
    return df.to_html(classes="table table-striped")

def hemi_data(browser):
    # The only way to get the following code to run was to
    # import the dependencies again
    
    # Import Splinter and BeautifulSoup
    from splinter import Browser
    from bs4 import BeautifulSoup as soup
    from webdriver_manager.chrome import ChromeDriverManager
    import pandas as pd
    import re
    
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    url = 'https://marshemispheres.com/'
    browser.visit(url)

    html = browser.html
    soup = soup(html, "html.parser")

    img_url_rel=soup.select("div.item [href]")

    urls_all = [link['href'] for link in img_url_rel]
#     urls_all

    urls = pd.unique(urls_all).tolist()
#     urls

    image_url = []

    for i in urls:
          image_url.append(f'https://marshemispheres.com/{i}')

#     print(image_url)

    ttls = soup.find_all('h3')
    image_title = []

    for titles in ttls:
        image_title.append(titles.text)  

    image_title.remove('Back')
#     print(image_title)

    # Import Splinter and BeautifulSoup
    from splinter import Browser
    from bs4 import BeautifulSoup as soup
    from webdriver_manager.chrome import ChromeDriverManager
    import pandas as pd
    import re

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

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

    browser.quit()

    return hemisphere_image_urls
    
if __name__ == "__main__":
    
    # If running as script, print scraped data
    print(scrape_all())

