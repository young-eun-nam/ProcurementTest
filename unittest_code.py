
import collections
import unittest
import os
import re

def custom_function(file_name):
    with open(file_name, 'rt') as f:
        '''파일의 라인을 합산해서 리턴합니다.'''
        return sum(1 for _ in f)


# TestCase를 작성
class CustomTests(unittest.TestCase):

    def setUp(self):
        """테스트 시작되기 전 파일 작성"""
        self.file_name = 'test_file.txt'
        with open(self.file_name, 'wt') as f:
            f.write("""
            파이썬에는 정말 단위테스트 모듈이 기본으로 포함되어 있나요? 진짜?
            멋지군요!
            단위테스트를 잘 수행해보고 싶습니다!
            """.strip())

    def tearDown(self):
        """테스트 종료 후 파일 삭제 """
        
        try:
            os.remove(self.file_name)
        except:
            pass
        
    # 이름이 test로 시작하는 경우 실행
    # 이름 순으로 실행
    # def test_runs(self):
    #     """단순 실행여부 판별하는 테스트 메소드"""
    #
    #     custom_function(self.file_name)
    #
    # def test_no_file(self):
    #     with self.assertRaises(IOError):
    #         custom_function(self.file_name)
    #
    # def test_line_count(self):
    #     self.assertEqual(custom_function(self.file_name), 3)

    def test_on_bool(self):
        self.assertTrue(1)

    def test_on_bool2(self):
        self.assertFalse(0)
        self.assertFalse([])

    def test_on_equal(self):
        self.assertIs(1, 1)
        self.assertIs(self, self)

    def test_on_equal2(self):
        self.assertIsNot(0, 1)

    def test_on_instance(self):
        class Tmp(tuple):
            pass
        tmpObject = Tmp()
        self.assertIsInstance(tmpObject, Tmp)
        self.assertIsInstance(tmpObject, tuple)

    def test_on_regex(self):
        '''
        정규표현식 관련 자료
        https://wikidocs.net/4308

        :return: None
        '''
        self.assertRegex('abbbbc', 'ab{2,10}c')
        self.assertRegex('abc', 'a.c')
        self.assertRegex('a1c', 'a.c')
        self.assertRegex('abbbbc', 'ab*c')
        self.assertRegex('ac', 'a.*c')

    def assertCountEqual(self, first, second, msg=None):
        '''
        a and b have the same elements in the same number, regardless of their order
        '''
        first = [1, 2, 3]
        second = (1, 2, 3)

        self.assertCountEqual(first, second)


    # unittest를 실행
if __name__ == '__main__':

    unittest.main()

    # p = re.compile('[a-z]+')
    # m = p.match('python84')
    # print(m, m.group())
    # s = p.search('123 python 123 json')
    # print(s, s.group())
    # print(s.start(), s.end())

