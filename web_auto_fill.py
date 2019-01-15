import unittest
import time
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import posixpath
from pyvirtualdisplay import Display

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

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
IMAGE_SAMPLE_DIR = posixpath.join(ROOT_DIR + '/image_sample')
IMAGE_SAMPLE_NAMES = ('견적서_결제.png', '세금계산서.png', '입고사진.png', '거래명세서.png')
PATH_IMG_FILES = [posixpath.join(IMAGE_SAMPLE_DIR, file_name) for file_name in IMAGE_SAMPLE_NAMES]


def add_multiple_item(driver, values=['모델명', '제조사', '규격', None, '20', '10', None, None]):
    def put_value_in_elements(values, input_elements):
        for value, element in zip(values, input_elements):
            if value is None:
                continue
            else:
                element.send_keys(Keys.CONTROL + "a")
                element.send_keys(Keys.DELETE)
                element.send_keys(value)

    # 품목 추가 버튼
    x_path = '//button[@class="v-btn v-btn--flat v-btn--outline v-btn--depressed theme--light grey--text"]'
    driver.find_element_by_xpath(x_path).click()
    driver.find_element_by_xpath(x_path).click()

    # 각 라인 추가
    x_path = '//div[@class="layout row wrap justify-center"]/div[@class="flex px-1 xs12 sm8 md3"]/..'
    elements = driver.find_elements_by_xpath(x_path)

    # element 추가
    for index, element in enumerate(elements):
        tmp_values = []
        for value in values:
            if value is not None:
                tmp_values.append(value + str(index))
            else:
                tmp_values.append(value)

        input_elements = element.find_elements_by_tag_name("input")
        put_value_in_elements(tmp_values, input_elements)


def choose_tap(driver, index):
    xpath_tap = XPATH_TAB_TEMPLATE.format(TAP_HREF_NAME[index])
    element = driver.find_element_by_xpath(xpath_tap)
    element.click()

def click_cancle_button(driver, name_button='품의취소'):
    # '구매 발주-결제'에서 - 품의취소
    # '입고 검수'에서 - 구매취소
    elements = driver.find_elements_by_xpath('//button[@class="mx-1 v-btn v-btn--block theme--dark"]')
    for element in elements:
        element.text.__contains__(name_button)
        element.click()
        break

class PythonWebTest(unittest.TestCase):

    def setUp(self):
        '''
        for linux without display
        display = Display(visible=0, size=(2560, 1440))
        display.start()
        self.driver = webdriver.Chrome('/home/dev/chromedriver',
                                  service_args=['--verbose', '--log-path=/tmp/chromedriver.log'])
        '''
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
                if label_name == '수량':
                    element.send_keys(Keys.CONTROL + "a")
                    element.send_keys(Keys.DELETE)
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

        # 통화 변경
        driver.find_element_by_xpath('//div[@class="v-select__selection v-select__selection--comma"]').click()
        elements = driver.find_elements_by_xpath('//div[@class="v-list__tile__title"]')
        # elements 311 개 search 됨 줄일 수 있으면 줄일 것
        # print(len(elements))
        # reverse로 하는 이유는 시간 절약을 위해서
        elements.reverse()
        for element in elements:
            if element.text == 'CNY':
                element.click()

        # 품목추가 버튼 누를 경우 (item 여러개 추가하는 경우)
        add_multiple_item(driver, ['모델명', '제조사', '규격', None, '20', '10', None, None])

        # 이미지 업로드
        element = driver.find_element_by_xpath('//input[@id="EstimateImage"]')
        file_path = os.path.abspath(PATH_IMG_FILES[0])
        element.send_keys(file_path)

        # 품의제출 버튼 클릭
        elements = driver.find_elements_by_xpath('//button[@class="v-btn v-btn--block theme--dark"]')
        for element in elements:
            if element.text.__contains__('품의제출'):
                element.click()

        # 엑셀에 반영될 때 까지 각 단계에서 24, 17, 21초
        time.sleep(25)

    # @unittest.skip('skip')
    def test_fill_2_payment(self):
        print('payment')
        driver = self.driver
        driver.get(PROCUREMENT_URL)

        element = driver.find_element_by_xpath(XPATH_INPUT_TEMPLATE.format('이름'))
        element.send_keys('김철')
        element.send_keys(Keys.ENTER)

        # 탭 이동 payment page로
        choose_tap(driver, 1)

        # 제출한 품의가 있을 경우 가장 최신 품의
        element = driver.find_element_by_xpath(XPATH_INPUT_TEMPLATE.format('품의 번호'))
        element.click()
        # spread sheet에서 loading 되어지는데 필요한 시간
        time.sleep(2)

        element.send_keys(Keys.ARROW_DOWN)
        element.send_keys(Keys.ENTER)
        # 선택된 품의가 있는지 확인하고 없으면 넘어가는 부분이 있어야 하는데 생략

        # 결제방법 선택
        element = driver.find_element_by_xpath(XPATH_INPUT_TEMPLATE.format('결제 방법'))
        element.send_keys(Keys.ARROW_DOWN)
        element.send_keys(Keys.ENTER)

        # (option) 거래처 변경 할 수도 있음

        # 현제 발주일, 결제일 고정 (
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

        # 이미지 업로드 (세금계산서)
        element = driver.find_element_by_xpath('//input[@id="billImage"]')
        file_path = os.path.abspath(PATH_IMG_FILES[1])
        element.send_keys(file_path)

        # 결제보고 버튼 클릭
        elements = driver.find_elements_by_xpath('//button[@class="v-btn v-btn--block theme--dark"]')
        for element in elements:
            if element.text.__contains__('결제보고'):
                element.click()

        # 엑셀에 반영될 때 까지 각 단계에서 24, 17, 21초
        time.sleep(25)

    @unittest.skip('skip')
    def test_fill_2_payment_cancle(self):
        print('payment')
        driver = self.driver
        driver.get(PROCUREMENT_URL)

        element = driver.find_element_by_xpath(XPATH_INPUT_TEMPLATE.format('이름'))
        element.send_keys('김철')
        element.send_keys(Keys.ENTER)

        # 탭 이동 payment page로
        choose_tap(driver, 1)

        # 제출한 품의가 있을 경우 가장 최신 품의
        element = driver.find_element_by_xpath(XPATH_INPUT_TEMPLATE.format('품의 번호'))
        element.click()
        # spread sheet에서 loading 되어지는데 필요한 시간
        time.sleep(2)

        element.send_keys(Keys.ARROW_DOWN)
        element.send_keys(Keys.ENTER)

        click_cancle_button(driver, '품의취소')

        time.sleep(25)

    # @unittest.skip('skip')
    def test_fill_3_receipt(self):
        print('receipt')
        driver = self.driver
        driver.get(PROCUREMENT_URL)

        element = driver.find_element_by_xpath(XPATH_INPUT_TEMPLATE.format('이름'))
        element.send_keys('김철')
        element.send_keys(Keys.ENTER)

        # 탭 이동 payment page로
        choose_tap(driver, 2)

        # 제출한 품의가 있을 경우 가장 최신 품의
        elements = driver.find_elements_by_xpath(XPATH_INPUT_TEMPLATE.format('품의 번호'))
        # spread sheet에서 loading 되어지는데 필요한 시간
        time.sleep(2)
        # '품의 번호' input이 구매 발주-결제 에도 있어서 2개가 검색 되므로 2번째 input을 사용하자
        element = elements[1]
        element.send_keys(Keys.ARROW_DOWN)
        element.send_keys(Keys.ENTER)

        label = "검수 결과 (예: 이상 없음.)"
        input = '이상 없음'
        element = driver.find_element_by_xpath(XPATH_TEXTAREA_TEMPLATE.format(label))
        element.send_keys(input)

        label = "입고 위치"
        input = '서울'
        element = driver.find_element_by_xpath(XPATH_INPUT_TEMPLATE.format(label))
        element.send_keys(input)
        element.send_keys(Keys.ENTER)

        label = "부분 입고 내용 및 비고 사항"
        input = '모든 물품 입고 완료'
        element = driver.find_element_by_xpath(XPATH_TEXTAREA_TEMPLATE.format(label))
        element.send_keys(input)

        # 이미지 업로드 (입고 사진)
        element = driver.find_element_by_xpath('//input[@id="logImage"]')
        file_path = os.path.abspath(PATH_IMG_FILES[2])
        element.send_keys(file_path)

        # 이미지 업로드 (거래명세서)
        element = driver.find_element_by_xpath('//input[@id="tradeStatementImage"]')
        file_path = os.path.abspath(PATH_IMG_FILES[3])
        element.send_keys(file_path)

        # 입고보고 버튼 클릭
        elements = driver.find_elements_by_xpath('//button[@class="v-btn v-btn--block theme--dark"]')
        for element in elements:
            if element.text.__contains__('입고보고'):
                element.click()

        time.sleep(10)

    @unittest.skip('skip')
    def test_fill_3_receipt_cancle(self):
        print('receipt')
        driver = self.driver
        driver.get(PROCUREMENT_URL)

        element = driver.find_element_by_xpath(XPATH_INPUT_TEMPLATE.format('이름'))
        element.send_keys('김철')
        element.send_keys(Keys.ENTER)

        # 탭 이동 payment page로
        choose_tap(driver, 2)

        # 제출한 품의가 있을 경우 가장 최신 품의
        elements = driver.find_elements_by_xpath(XPATH_INPUT_TEMPLATE.format('품의 번호'))
        # spread sheet에서 loading 되어지는데 필요한 시간
        time.sleep(2)
        # '품의 번호' input이 구매 발주-결제 에도 있어서 2개가 검색 되므로 2번째 input을 사용하자
        element = elements[1]
        element.send_keys(Keys.ARROW_DOWN)
        element.send_keys(Keys.ENTER)

        click_cancle_button(driver, '구매취소')


if __name__ == '__main__':

    unittest.main()
