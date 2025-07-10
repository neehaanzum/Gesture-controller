from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def open_youtube_video(video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"):
    options = Options()
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(video_url)
    time.sleep(5)

    try:
        play_button = driver.find_element(By.CSS_SELECTOR, 'button.ytp-play-button')
        play_button.click()
        print("[INFO] YouTube video started.")
    except Exception as e:
        print("[WARNING] Could not click play button:", e)

    return driver
