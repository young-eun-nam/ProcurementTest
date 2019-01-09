import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os

PROCUREMENT_URL = "http://141.223.199.172:3210/#/procurement"

INPUT_LABEL_NAMES_AND_INPUT = (('이름', '김철'),
                               ('품목명', '품목명1'),
                               ('프로젝트/제품', '기타'),
                               ('사용 목적', '교육훈련비'),
                               ('결재담당자', '윤진성'),
                               ('모델명',  '모델명1'),
                               ('제조사', '제조사1'),
                               ('규격', '규격1'),
                               # ('통화_', 'USD'),
                               ('단가', '100'),
                               ('수량',  '2'),
                               # ('공급가액', '품목명1'),
                               ('결제 계정-공급가액',  '투자_QD'),
                               ('결제 계정-부가세', '투자_QD'),
                               ('배송료(c)',  '2000'),
                               ('결제 계정-배송료', '과제_TIPS'),
                               ('기타수수료(d)',  '3000'),
                               # ('통화',  'USD'),
                               ('결제 계정-기타수수료', '투자_LH'),
                               ('거래처',  '한랩서비스')
                               )

XPATH_INPUT_TEMPLATE = '//input[@aria-label="{}"]'

TEXTAREA_LABEL_NAMES_AND_INPUT = (('제품 링크',  'http://141.223.199.172:3210/#/procurement'), ('세부 내용 및 비고', '비고 없음'))

XPATH_TEXTAREA_TEMPLATE = '//textarea[@aria-label="{}"]'

TAP_HREF_NAME = ('proposal', 'payment', 'receipt')

XPATH_TAB_TEMPLATE = '//a[@href="#{}"]'

PATH_IMG = 'C:\\Temp\\example.png'


class PythonWebTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        print('open browser')

    def tearDown(self):
        try:
            self.driver.close()
            print('close browser')
        except Exception as e:
            print('tearDown Error', e)

    # @unittest.skip('skip')
    def test_fill_1_proposal(self):
        print('proposal')
        driver = self.driver
        driver.get(PROCUREMENT_URL)
        time.sleep(1)

        for label_name, input in INPUT_LABEL_NAMES_AND_INPUT:
            try:
                element = driver.find_element_by_xpath(XPATH_INPUT_TEMPLATE.format(label_name))
                element.send_keys(input)
                time.sleep(0.05)
                element.send_keys(Keys.ENTER)
                time.sleep(0.05)
            except Exception as e:
                print(label_name, input, e)

        for label_name, input in TEXTAREA_LABEL_NAMES_AND_INPUT:
            try:
                element = driver.find_element_by_xpath(XPATH_TEXTAREA_TEMPLATE.format(label_name))
                element.send_keys(input)
            except Exception as e:
                print(label_name, input, e)

        # 통화 변경
        driver.find_element_by_xpath('//div[@class="v-select__selection v-select__selection--comma"]').click()
        elements = driver.find_elements_by_xpath('//div[@class="v-list__tile__title"]')
        # elements 311 개 search 됨 줄일 수 있으면 줄일 것
        # print(len(elements))
        # reverse로 하는 이유는 시간 절약을 위해서
        for element in elements.reverse():
            if element.text == 'CNY':
                element.click()


        # 품목추가 버튼 누를 경우 (item 여러개 추가하는 경우)

        # 이미지 업로드
        element = driver.find_element_by_xpath('//input[@id="EstimateImage"]')
        file_path = os.path.abspath(PATH_IMG)
        element.send_keys(file_path)

        # 품의제출 버튼 클릭
        # element = driver.find_element_by_xpath('//button[@class="v-btn v-btn--block theme--dark"]')
        # element.click()

        time.sleep(10)

    # @unittest.skip('skip')
    def test_fill_2_payment(self):
        print('payment')
        driver = self.driver
        driver.get(PROCUREMENT_URL)
        
        # 탭 이동 payment page로
        xpath_second_tap = XPATH_TAB_TEMPLATE.format(TAP_HREF_NAME[1])
        element = driver.find_element_by_xpath(xpath_second_tap)
        print('1', element.text)
        element.click()

        # 제출한 품의가 있을 경우 가장 최신 품의
        element = driver.find_element_by_xpath(XPATH_INPUT_TEMPLATE.format('품의 번호'))
        element.click()
        # spread sheet에서 loading 되어지는데 필요한 시간
        time.sleep(2)

        element.send_keys(Keys.ARROW_DOWN)
        element.send_keys(Keys.ENTER)
        # 선택된 품의가 있는지 확인하고 없으면 넘어가는 부분이 있어야 하는데 생략

        # 결제방법 선택
        element = driver.find_element_by_xpath(XPATH_INPUT_TEMPLATE.format('품의 번호'))
        element.click()
        element.send_keys(Keys.ARROW_DOWN)
        element.send_keys(Keys.ENTER)

        # (option) 거래처 변경 할 수도 있음

        # 발주일 클릭
        element = driver.find_element_by_xpath(XPATH_INPUT_TEMPLATE.format('발주일'))
        element.click()
        time.sleep(0.5)
        elements = driver.find_elements_by_xpath('//button[@type="button"]/div[@class="v-btn__content"]')
        for element in elements:
            if element.text == '1':
                element.click()
                break

        # 결제일
        element = driver.find_element_by_xpath(XPATH_INPUT_TEMPLATE.format('결제일'))
        element.click()
        time.sleep(0.5)
        elements = driver.find_elements_by_xpath('//button[@type="button"]/div[@class="v-btn__content"]')
        for element in elements:
            if element.text == '10':
                element.click()
                break

        # 발주자
        # (default- 발주자/결제자 선택시 자동 입력) 연락처 번호, 연락처 이메일
        element = driver.find_element_by_xpath(XPATH_INPUT_TEMPLATE.format('발주자'))
        element.send_keys('김철')
        element.send_keys(Keys.ENTER)
        # 결제자
        element = driver.find_element_by_xpath(XPATH_INPUT_TEMPLATE.format('결제자'))
        element.send_keys('윤진성')
        element.send_keys(Keys.ENTER)

        # 비고
        element = driver.find_element_by_xpath(XPATH_TEXTAREA_TEMPLATE.format('추가 내용 및 비고'))
        element.send_keys('추가 내용 및 비고 없음')

        time.sleep(20)


if __name__ == '__main__':

    unittest.main()
