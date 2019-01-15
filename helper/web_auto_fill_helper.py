
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
