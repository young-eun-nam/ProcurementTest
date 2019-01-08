from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

PROCUREMENT_URL = "http://141.223.199.172:3210/#/procurement"
'''
INPUT_LABEL_NAMES = ['품목명', '프로젝트/제품', '사용 목적', '결재담당자', '통화_', '공급가액', '부가세', '공급가액합계(a)',
                     '결제 계정-공급가액', '부가세 합계(b)', '결제 계정-부가세', '배송료(c)', '결제 계정-배송료', '기타수수료(d)',
                     '결제 계정-기타수수료', '통화', '총액(VAT 포함)', '거래처', '제품 링크', '세부 내용 및 비고', '품의 번호', '품목',
                     '통화', '총액(VAT 포함)', '발주자 선택', '발주자', '발주 일자', '프로젝트/제품', '사용 목적', '결제 계정',
                     '거래처', '제품 링크', '세부 내용 및 비고', '추가 내용 및 비고', '품의 번호', '품목', '통화', '총액(VAT 포함)',
                     '프로젝트/제품', '사용 목적', '검수자', '입고 위치', '입고 일자', '제품 링크', '품의 내용 및 비고',
                     '발주 내용 및 비고', '검수 결과 (예: 이상 없음.)', '부분 입고 내용 및 비고 사항']
'''

INPUT_LABEL_NAMES_AND_INPUT = (('이름', '김철'),
                               ('품목명', '품목명1'),
                               ('프로젝트/제품', '기타'),
                               ('사용 목적', '교육훈련비'),
                               ('결재담당자', '윤진성'),
                               ('모델명',  '모델명1'),
                               ('제조사', '제조사1'),
                               ('규격', '규격1'),
                               # ('통화_', '품목명1'),
                               ('단가', '100'),
                               ('수량',  '2'),
                               # ('공급가액', '품목명1'),
                               ('결제 계정-공급가액',  '투자_QD'),
                               ('결제 계정-부가세', '투자_QD'),
                               ('배송료(c)',  '2000'),
                               ('결제 계정-배송료', '투자_QD'),
                               ('기타수수료(d)',  '3000'),
                               ('결제 계정-기타수수료', '투자_QD'),
                               # ('통화',  'USD'),
                               ('거래처',  '한랩서비스')
                               )

XPATH_INPUT_TEMPLATE = '//input[@aria-label="{}"]'

TEXTAREA_LABEL_NAMES_AND_INPUT = (('제품 링크',  'http://naver.com'), ('세부 내용 및 비고', '비고 없음'))

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