import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
driver = webdriver.Chrome(options=options)


#link of the subreddit
driver.get("https://www.reddit.com/r/blackops6/search/?q=+&type=media&cId=9eb476fd-2f24-4726-83aa-a577343d949c&iId=488456f0-ad50-421a-afd5-8e11b19a590b&t=week&sort=top")
time.sleep(1)  # Let the page load. In real code, prefer WebDriverWait over sleep.
post_links = []
titles = []
video_sources = []

def get_videos_and_titles():
    #Scroll so the posts are loaded
    driver.execute_script("window.scrollTo(0, 1800)")
    time.sleep(5)

    #Collect URLS of posts

    posts = driver.find_elements(By.TAG_NAME, 'source')

    for post in posts:
        src = post.get_attribute("src")
        if src and ".mp4" in src:
            try:
                # Find the nearest ancestor anchor
                link_elem = post.find_element(By.XPATH, './/ancestor::a[1]')
                href = link_elem.get_attribute("href")
                post_links.append(href)
            except:
                pass

    #iterate over URLs
    for post_url in post_links:
        # Navigate directly to the post’s page
        driver.get(post_url)
        time.sleep(2)

        #Grab the title
        try:
            title_element = driver.find_element(By.TAG_NAME, 'h1')
            title = title_element.text
            titles.append(title)
        except:
            title = "(No title found)"
            titles.append("title not found")

        #get the video
        try:
            shadow_host = driver.find_element(By.CSS_SELECTOR, "shreddit-player-2")
            shadow_root = driver.execute_script("return arguments[0].shadowRoot", shadow_host)

            if shadow_root:
                video_element = shadow_root.find_element(By.CSS_SELECTOR, "video")
                video_src = video_element.get_attribute("src")
                video_sources.append(video_src)
            else:
                video_src = "(No shadow root)"
                video_sources.append("source not found")

        except:
            print("Could not locate video on detail page of:", post_url)


#def download_videos():
    

for i in range(len(video_sources)):
    print("Title: "+titles[i])
    print("URL: "+video_sources[i])
    print("--------")





driver.quit()