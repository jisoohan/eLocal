import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class UITest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def testHomePage(self):
        driver = self.driver
        driver.get('http://localhost:8000')
        inputElement_ZipCode = driver.find_element_by_id("zip_code")
        inputElement_ZipCode.send_keys("94704")
        inputElement_Radius = driver.find_element_by_id("radius")
        inputElement_Radius.send_keys("1")
        submit = driver.find_element_by_id("submitForm")
        submit.submit()

    def tearDown(self):
        self.driver.close()

if __name__ == '__main__':
    unittest.main()
