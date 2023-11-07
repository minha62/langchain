from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
import os

def SimpleDetail(url):
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

    # 상품 별점 가져오기
    score = driver.find_element(By.CLASS_NAME, 'prd-score__rating').text + "/5.0"

    # 후기 개수 가져오기
    review_count = driver.find_element(By.CLASS_NAME, 'prd-score__review-count').text.replace(" 보기", "")

    # 상품 카테고리 가져오기
    categories = driver.find_element(By.CLASS_NAME, 'article-tag-list').text.replace("\n", " ")

    # 많이 구매한 고객의 연령대, 성별 가져오기
    popular = driver.find_element(By.CSS_SELECTOR, '#graph_summary_area').text.replace(' 에게 인기 많은 상품', '')

    # 도착 예정일 가져오기
    delivery = driver.find_element(By.CSS_SELECTOR, 'div.CArrivalInformation__text').text.replace(' 도착 예정', '')

    # 가격 가져오기
    price = driver.find_element(By.CSS_SELECTOR, '#list_price').text

    # 사이즈 정보 가져오기
    size_table = driver.find_element(By.CSS_SELECTOR, '#size_table tbody')
    size_rows = size_table.find_elements(By.TAG_NAME, 'tr')
    size_data = {}
    for row in size_rows[2:]:
        size_name = row.find_element(By.TAG_NAME, 'th').text
        size_values = [td.text for td in row.find_elements(By.CLASS_NAME, 'goods_size_val')]
        size_data[size_name] = size_values

    output = "[평점]\n" + score + "  (" + review_count + ")\n\n" + "[구매층]\n" + popular + "\n\n[사이즈 옵션]\n" + str(list(size_data.keys())).replace('\'','').replace('[','').replace(']','') + "\n\n[도착 예정일]\n" + delivery + "\n\n[카테고리]\n" + categories

    first_up_review = driver.find_elements(By.CSS_SELECTOR, 'div.review-list')[0]
    if first_up_review:
        review = {}
        try:
            profile_element = first_up_review.find_element(By.CSS_SELECTOR, 'p.review-profile__body_information')
            review["profile"] = profile_element.text
        except:
            review["profile"] = "비회원"

        try:
            size_element = first_up_review.find_element(By.CSS_SELECTOR, 'span.review-goods-information__option')
            review["size"] = size_element.text
        except:
            review["size"] = "None"

        try:
            content = first_up_review.find_element(By.CSS_SELECTOR, 'div.review-contents__text')
            review["content"] = content.text.replace('\n', '')
        except:
            review["content"] = "None"

        try:
            review_img = first_up_review.find_element(By.CLASS_NAME, 'review-content-photo__item').find_element(By.TAG_NAME, 'img').get_attribute('src')
            review["img"] = 'https:' + review_img
        except:
            review["img"] = "None"
        
        output += '\n\n[가장 유용한 리뷰]\n' + review['profile'] + ' · ' + review['size'] + ' 구매\n\"' + review['content'] + '\"'
    
    return {"simple_detail":output, "img":review['img']}