from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import webbrowser


    


class WebDriver:
    def __init__(self):
        
      
        self.service = Service('C:\\WebDrivers\\chromedriver-win64\\chromedriver.exe')
        
        self.driver = None
        

    def get_info(self, query):
        print(f"Query received: {query}")  # Print the query to verify it's being passed correctly
        self.query = query
        self.driver=webdriver.Chrome(service=self.service)
        self.driver.get("https://www.wikipedia.org/")

        # Wait for the search input field to be clickable
        look_for = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="searchInput"]'))
        )
        look_for.click()
        look_for.send_keys(query)

        # Wait for the search button to be clickable and click it
        enter = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="search-form"]/fieldset/button'))
        )
        enter.click()

        # Keep the browser open for verification
        time.sleep(300)

        # Close the browser after the action is done
        self.driver.quit()
   
   
   
    def play_yt(self, query):
        print(f"Query received: {query}")  # Print the query to verify it's being passed correctly
        self.query = query

        # Initialize the browser
        self.driver = webdriver.Chrome(service=self.service)
        self.driver.get("https://www.youtube.com/results?search_query=" + query)

        try:
            # Wait for the video title element to load
            video_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'video-title'))
            )
            
            # Click the video to start playing
            video_element.click()
            print(f"Playing video for query: {query}")
            
            # Let the video play for a while
            time.sleep(280)  
        except Exception as e:
            print(f"An error occurred while playing YouTube video: {e}")
        finally:
            # Close the browser
            self.driver.quit()


    def web_launcher(self, query):
       
        websites = {
            'YouTube': "https://www.youtube.com/",
            'Google': "https://www.google.com",
            'stack overflow': "https://stackoverflow.com",
            'facebook': "https://facebook.com",
            'anime': "https://9animetv.to/home",
            'AI': "https://chatgpt.com/",
        }

        for key, url in websites.items():
            if key.lower() in query.lower():
                print(f"Opening {key}...")
                webbrowser.open(url)
                return

        print("Website not recognized. Opening Google as a fallback.")
        webbrowser.open("https://www.google.com")
