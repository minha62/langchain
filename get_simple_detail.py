from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
import os

def GetSimpleDetail(url):
    # Chrome 옵션 설정
    options = webdriver.ChromeOptions()
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN") # for heroku
    options.add_argument('--headless')  # 브라우저 창 숨기기
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')

    service = Service(executable_path=os.environ.get("CHROMEDRIVER_PATH"))

    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) # local
    driver = webdriver.Chrome(service=service, options=options) # for heroku
    driver.get(url)

    # 상품 정보 가져오기
    # product_info = driver.find_element(By.CSS_SELECTOR, 'ul.product_article').text.replace('\n', '')

    # 많이 구매한 고객의 연령대, 성별 가져오기
    # popular = driver.find_element(By.CSS_SELECTOR, '#graph_summary_area').text

    # 도착 예정일 가져오기
    delivery = driver.find_element(By.CSS_SELECTOR, 'div.CArrivalInformation__text').text

    # 가격 가져오기
    # price = driver.find_element(By.CSS_SELECTOR, '#list_price').text

    # 사이즈 정보 가져오기
    size_info = driver.find_element(By.CSS_SELECTOR, '#size_table')
    driver.execute_script("arguments[0].querySelector('#mysize').remove();", size_info)
    size_info = size_info.text

    first_up_review = driver.find_elements(By.CSS_SELECTOR, 'div.review-list')[0]
    if first_up_review:
        content_element = first_up_review.find_element(By.CSS_SELECTOR, 'div.review-contents__text')
        best_review = content_element.text.replace(' ', '').replace('\n', '')
    else:
        best_review = None

    return {
        #"product_info": product_info,
        #"popular": popular,
        "delivery": delivery,
        #"price": price,
        "size_info": size_info,
        "best_review": best_review
    }