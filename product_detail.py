from playwright.async_api import async_playwright

async def ProductDetails(url):
    def reviewObject(page, reviewElement):
        reviews = []
        for re in reviewElement:
            review = {}

            profile_element = re.query_selector("p.review-profile__body_information")
            if profile_element:
                review["profile"] = profile_element.inner_text()
            else:
                review["profile"] = "None"
            
            size_element = re.query_selector("span.review-goods-information__option")
            if size_element:
                review["size"] = size_element.inner_text()
            else:
                review["size"] = "None"

            score = re.query_selector("span.review-list__rating__active")
            if score:
                score_percent = page.evaluate('(element) => element.style.width', score)
                review["score"] = score_percent
            else:
                review["score"] = "None"
            
            content_element = re.query_selector("div.review-contents__text")
            if content_element:
                review["content"] = content_element.inner_text()
            else:
                review["content"] = "None"

            reviews.append(review)
        return reviews

    async with async_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        #context = browser.new_context()
        page = browser.new_page()

        await page.goto(url)

        contents = page.query_selector("#product_order_info")

        # 상품 정보
        product_info = contents.query_selector("ul.product_article").inner_text()
        product_info = product_info.replace('\n', '')

        # 많이 구매한 고객의 연령대, 성별
        popular = contents.query_selector("#graph_summary_area").inner_text()

        # 도착 예정일
        delivery = contents.query_selector("div.CArrivalInformation__text").inner_text()
        #formatted_delivery = f"도착 예정 날짜: {delivery}"

        # 가격
        price = contents.query_selector("#list_price").inner_text()

        # 사이즈 추천 30개
        size_reco = []
        size_reco_elements = contents.query_selector_all("p.size_content")
        for content in size_reco_elements[:30]:
            size_reco.append(content.inner_text())


        # 사이즈 정보
        size_info = page.query_selector("#size_table")
        page.evaluate('(element) => element.querySelector("#mysize").remove()', size_info)
        size_info = size_info.inner_text()

        # 유용한 순 리뷰 10개
        up_reviews_10 = page.query_selector_all("div.review-list")[:10]
        up_reviews = reviewObject(page, up_reviews_10)

        # 평점 낮은 순 리뷰 10개
        page.select_option("#reviewSelectSort", "goods_est_asc")
        worst_reviews_10 = page.query_selector_all("div.review-list")[:10]
        worst_reviews = reviewObject(page, worst_reviews_10)

        browser.close()

        return {
            "details": {
                "product_info": product_info,
                "popular": popular,
                "delivery": delivery,
                "price": price,
            },
            "size" : {
                "size_reco": size_reco,
                "size_info": size_info,
            },
            "up_reviews": up_reviews,
            "worst_reviews": worst_reviews,
        }