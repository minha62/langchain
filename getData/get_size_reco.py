from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import re

def GetSizeReco(url, local=False):
    # Chrome 옵션 설정
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 브라우저 창 숨기기
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')

    if local:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    else:
        service = Service(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
        options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    # 사이즈 추천 30개 가져오기
    size_reco = []
    size_reco_elements = driver.find_elements(By.CSS_SELECTOR, 'p.size_content')
    if size_reco_elements:
        size_pattern = r'\[(.*?)\]\s*\((.*?)\)\s*(.*?)\s*(.*?)\s*구매'
        for content in size_reco_elements[:30]:
            matches = re.search(size_pattern, content.text)
            if matches:
                size = matches.group(2) + matches.group(4)
                size_reco.append(size)
            else: break
    else:
        size_reco = None

    return {
            "size_reco": size_reco,
        }