from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os

PROCUREMENT_URL = "http://141.223.199.172:3210/#/procurement"
PRODUCT_URL = "http://www.gsshop.com/deal/deal.gs?dealNo=30845205&kwd=%EB%A7%88%EC%9A%B0%EC%8A%A4&ab=a&gsid=srcheshop-result&lseq=396001"
IMG_PATH = '/Users/admin/Screenshot_2.png'

INPUT_LABEL_NAMES_AND_INPUT = (('이름', '남영은'),
                               ('품목명', '품목명1'),
                               ('프로젝트/제품', '기타'),
                               ('사용 목적', '교육훈련비'),
                               ('결재담당자', '윤진성'),
                               ('모델명',  '모델명1'),
                               ('제조사', '제조사1'),
                               ('규격', '규격1'),
                               # ('통화_', 'USD'),
                               ('단가', '10000'),
                               ('수량',  '1'),
                               # ('공급가액', '품목명1'),
                               ('결제 계정-공급가액', '법인_매출'),
                               ('결제 계정-부가세', '법인_매출'),
                               ('배송료(c)',  '2000'),
                               ('결제 계정-배송료', '법인_매출'),
                               ('기타수수료(d)',  '3000'),
                               ('결제 계정-기타수수료', '법인_매출'),
                               # ('통화',  'USD'),
                               ('거래처',  '한랩서비스')
                               )

XPATH_INPUT_TEMPLATE = '//input[@aria-label="{}"]'

TEXTAREA_LABEL_NAMES_AND_INPUT = (('제품 링크', PRODUCT_URL), ('세부 내용 및 비고', '비고 없음!'))

XPATH_TEXTAREA_TEMPLATE = '//textarea[@aria-label="{}"]'

driver = webdriver.Chrome('/Users/admin/chromedriver')
driver.get(PROCUREMENT_URL)

for label_name, input in INPUT_LABEL_NAMES_AND_INPUT:
    try:
        element = driver.find_element_by_xpath(XPATH_INPUT_TEMPLATE.format(label_name))
        if label_name == '수량':
            element.send_keys(Keys.BACK_SPACE)
        time.sleep(0.05)
        element.send_keys(input)
        time.sleep(0.05)
        element.send_keys(Keys.ENTER)
    except Exception as e:
        print(label_name, input, e)

for label_name, input in TEXTAREA_LABEL_NAMES_AND_INPUT:
    try:
        element = driver.find_element_by_xpath(XPATH_TEXTAREA_TEMPLATE.format(label_name))
        element.send_keys(input)
    except Exception as e:
        print(label_name, input, e)

# 이미지 업로드
element = driver.find_element_by_xpath('//input[@id="EstimateImage"]')
file_path = os.path.abspath(IMG_PATH)
element.send_keys(file_path)

# 품의제출 버튼 클릭
element = driver.find_element_by_xpath('//button[@class="v-btn v-btn--block theme--dark"]')
element.click()
time.sleep(10)
driver.close()