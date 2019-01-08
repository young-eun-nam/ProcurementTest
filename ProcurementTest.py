from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os

# CSS_SELECTOR 변수
submit_button_css_selector = '#app > div.application--wrap > div > div > div.layout.row.justify-center > div > div > div.v-card__text > div > div.v-window > div > div:nth-child(1) > div > form > div.v-card__actions.px-3 > button.v-btn.v-btn--block.theme--dark > div'

PROCUREMENT_URL = "http://141.223.199.172:3210/#/procurement"
PRODUCT_URL = "http://www.gsshop.com/deal/deal.gs?dealNo=30845205&kwd=%EB%A7%88%EC%9A%B0%EC%8A%A4&ab=a&gsid=srcheshop-result&lseq=396001"
'''
INPUT_LABEL_NAMES = ['품목명', '프로젝트/제품', '사용 목적', '결재담당자', '통화_', '공급가액', '부가세', '공급가액합계(a)',
                     '결제 계정-공급가액', '부가세 합계(b)', '결제 계정-부가세', '배송료(c)', '결제 계정-배송료', '기타수수료(d)',
                     '결제 계정-기타수수료', '통화', '총액(VAT 포함)', '거래처', '제품 링크', '세부 내용 및 비고', '품의 번호', '품목',
                     '통화', '총액(VAT 포함)', '발주자 선택', '발주자', '발주 일자', '프로젝트/제품', '사용 목적', '결제 계정',
                     '거래처', '제품 링크', '세부 내용 및 비고', '추가 내용 및 비고', '품의 번호', '품목', '통화', '총액(VAT 포함)',
                     '프로젝트/제품', '사용 목적', '검수자', '입고 위치', '입고 일자', '제품 링크', '품의 내용 및 비고',
                     '발주 내용 및 비고', '검수 결과 (예: 이상 없음.)', '부분 입고 내용 및 비고 사항']
'''

INPUT_LABEL_NAMES_AND_INPUT = (('이름', '남영은'),
                               ('품목명', '품목명1'),
                               ('프로젝트/제품', '기타'),
                               ('사용 목적', '교육훈련비'),
                               ('결재담당자', '윤진성'),
                               ('모델명',  '모델명1'),
                               ('제조사', '제조사1'),
                               ('규격', '규격1'),
                               # ('통화_', '품목명1'),
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
        element.send_keys(input)
        time.sleep(0.2)
        element.send_keys(Keys.ENTER)
    except Exception as e:
        print(label_name, input, e)

for label_name, input in TEXTAREA_LABEL_NAMES_AND_INPUT:
    try:
        element = driver.find_element_by_xpath(XPATH_TEXTAREA_TEMPLATE.format(label_name))
        element.send_keys(input)
    except Exception as e:
        print(label_name, input, e)

file_button_css_selector = '#EstimateImage'
file_upload = driver.find_element_by_css_selector(file_button_css_selector)
file_path = os.path.abspath('/Users/admin/Screenshot_2.png')
file_upload.send_keys(file_path)

submit = driver.find_element_by_css_selector(submit_button_css_selector)
submit.click()
time.sleep(10)
driver.close()