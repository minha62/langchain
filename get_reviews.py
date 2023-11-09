from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

def GetReviews(url, num=3, local=False):
    def reviewObject(reviewElements):
        reviews = []
        for re in reviewElements:
            review = {}

            try:
                profile_element = re.find_element(By.CSS_SELECTOR, 'p.review-profile__body_information')
                review["profile"] = profile_element.text
            except:
                review["profile"] = "비회원"

            try:
                size_element = re.find_element(By.CSS_SELECTOR, 'span.review-goods-information__option')
                review["size"] = size_element.text
            except:
                review["size"] = "None"

            try:
                score = re.find_element(By.CSS_SELECTOR, 'span.review-list__rating__active')
                score_percent = score.get_attribute('style').split('width:')[1].split('%')[0].strip()
                review["score"] = int(score_percent) // 20
            except:
                review["score"] = "None"

            try:
                content_element = re.find_element(By.CSS_SELECTOR, 'div.review-contents__text')
                review["content"] = content_element.text.replace('\n', '')
                # review_content = content_element.text.replace('\n', '')
                # reviews.append(review_content)
            except:
                review["content"] = "None"
                # reviews.append("")
            reviews.append(review)
        return reviews

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

    # 유용한 순 리뷰 가져오기
    data = driver.find_elements(By.CSS_SELECTOR, 'div.review-list')[:num]
    if data:
        up_reviews = reviewObject(data)
    else:
        up_reviews = None

   # "낮은 평점 순"으로 리뷰 정렬
    driver.find_element(By.CSS_SELECTOR, '#reviewSelectSort').click()
    low_rating_option = driver.find_element(By.CSS_SELECTOR, 'option[value="goods_est_asc"]')
    low_rating_option.click()
    time.sleep(2)  # 페이지 업데이트를 기다리기

    # 평점 낮은 순 리뷰 가져오기
    data = driver.find_elements(By.CSS_SELECTOR, 'div.review-list')[:num]
    if data:
        worst_reviews = reviewObject(data)
    else:
        worst_reviews = None

    return up_reviews, worst_reviews