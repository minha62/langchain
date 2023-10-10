from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.chrome.options import Options
#from webdriver_manager.chrome import ChromeDriverManager
import time
import os

def ProductDetails(url):
    def reviewObject(reviewElements):
        reviews = []
        for re in reviewElements:
            review = {}

            try:
                profile_element = re.find_element(By.CSS_SELECTOR, 'p.review-profile__body_information')
                review["profile"] = profile_element.text
            except:
                review["profile"] = "None"

            try:
                size_element = re.find_element(By.CSS_SELECTOR, 'span.review-goods-information__option')
                review["size"] = size_element.text
            except:
                review["size"] = "None"

            try:
                score = re.find_element(By.CSS_SELECTOR, 'span.review-list__rating__active')
                score_percent = score.get_attribute('style').split('width:')[1].split('%')[0].strip()
                review["score"] = score_percent
            except:
                review["score"] = "None"

            try:
                content_element = re.find_element(By.CSS_SELECTOR, 'div.review-contents__text')
                review["content"] = content_element.text
            except:
                review["content"] = "None"

            reviews.append(review)

        return reviews

    # Chrome 옵션 설정
    #options = Options()
    options = webdriver.ChromeOptions()
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN") # for heroku
    options.add_argument('--headless')  # 브라우저 창 숨기기
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')

    service = Service(executable_path=os.environ.get("CHROMEDRIVER_PATH"))

    #driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()), options=options) # local
    driver = webdriver.Chrome(service=service, options=options) # for heroku
    driver.get(url)

    # 상품 정보 가져오기
    product_info = driver.find_element(By.CSS_SELECTOR, 'ul.product_article').text.replace('\n', '')

    # 많이 구매한 고객의 연령대, 성별 가져오기
    popular = driver.find_element(By.CSS_SELECTOR, '#graph_summary_area').text

    # 도착 예정일 가져오기
    delivery = driver.find_element(By.CSS_SELECTOR, 'div.CArrivalInformation__text').text

    # 가격 가져오기
    price = driver.find_element(By.CSS_SELECTOR, '#list_price').text

    # 사이즈 추천 30개 가져오기
    size_reco = []
    size_reco_elements = driver.find_elements(By.CSS_SELECTOR, 'p.size_content')
    if size_reco_elements:
        for content in size_reco_elements[:30]:
            size_reco.append(content.text)
    else:
        size_reco = None

    # 사이즈 정보 가져오기
    size_info = driver.find_element(By.CSS_SELECTOR, '#size_table')
    driver.execute_script("arguments[0].querySelector('#mysize').remove();", size_info)
    size_info = size_info.text

    # 유용한 순 리뷰 10개 가져오기
    up_reviews_10 = driver.find_elements(By.CSS_SELECTOR, 'div.review-list')[:10]
    if up_reviews_10:
        up_reviews = reviewObject(up_reviews_10)
    else:
        up_reviews = None

    # 평점 낮은 순 리뷰 10개 가져오기
    driver.find_element(By.CSS_SELECTOR, '#reviewSelectSort').click()
    time.sleep(2)  # 페이지 업데이트를 기다립니다.
    worst_reviews_10 = driver.find_elements(By.CSS_SELECTOR, 'div.review-list')[:10]
    if worst_reviews_10:
        worst_reviews = reviewObject(worst_reviews_10)
    else:
        worst_reviews = None

    return {
            "details": {
                "product_info": product_info,
                "popular": popular,
                "delivery": delivery,
                "price": price,
            },
            "size": {
                "size_reco": size_reco,
                "size_info": size_info,
            },
            "up_reviews": up_reviews,
            "worst_reviews": worst_reviews,
        }

# url = 'https://www.musinsa.com/app/goods/3056893'
# result = ProductDetails(url)
# print(result)