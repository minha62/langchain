import subprocess
from playwright.async_api import async_playwright

subprocess.run(["playwright", "install"])

async def ProductDetails(url):
    async def reviewObject(page, reviewElement):
        reviews = []
        for re in reviewElement:
            review = {}

            profile_element = await re.query_selector("p.review-profile__body_information")
            if profile_element:
                review["profile"] = await profile_element.inner_text()
            else:
                review["profile"] = "None"
            
            size_element = await re.query_selector("span.review-goods-information__option")
            if size_element:
                review["size"] = await size_element.inner_text()
            else:
                review["size"] = "None"

            score = await re.query_selector("span.review-list__rating__active")
            if score:
                score_percent = await page.evaluate('(element) => element.style.width', score)
                review["score"] = score_percent
            else:
                review["score"] = "None"
            
            content_element = await re.query_selector("div.review-contents__text")
            if content_element:
                review["content"] = await content_element.inner_text()
            else:
                review["content"] = "None"

            reviews.append(review)
        return reviews

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=False)
        #context = browser.new_context()
        page = await browser.new_page()

        await page.goto(url)

        contents = await page.query_selector("#product_order_info")

        # 상품 정보
        product_info = await contents.query_selector("ul.product_article").inner_text()
        product_info = product_info.replace('\n', '')

        # 많이 구매한 고객의 연령대, 성별
        popular = await contents.query_selector("#graph_summary_area").inner_text()

        # 도착 예정일
        delivery = await contents.query_selector("div.CArrivalInformation__text").inner_text()
        #formatted_delivery = f"도착 예정 날짜: {delivery}"

        # 가격
        price = await contents.query_selector("#list_price").inner_text()

        # 사이즈 추천 30개
        size_reco = []
        size_reco_elements = await contents.query_selector_all("p.size_content")
        for content in size_reco_elements[:30]:
            size_reco.append(await content.inner_text())


        # 사이즈 정보
        size_info = await page.query_selector("#size_table")
        await page.evaluate('(element) => element.querySelector("#mysize").remove()', size_info)
        size_info = await size_info.inner_text()

        # 유용한 순 리뷰 10개
        up_reviews_10 = await page.query_selector_all("div.review-list")[:10]
        up_reviews = await reviewObject(page, up_reviews_10)

        # 평점 낮은 순 리뷰 10개
        await page.select_option("#reviewSelectSort", "goods_est_asc")
        worst_reviews_10 = await page.query_selector_all("div.review-list")[:10]
        worst_reviews = await reviewObject(page, worst_reviews_10)

        await browser.close()

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