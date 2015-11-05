import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class UITest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def testHomePage(self):
        driver = self.driver
        driver.get('http://localhost:8000')
        self.assertIn('eLocal', driver.title)

    #def testProductPage(self):
    #    driver = self.driver
    #    driver.get('http://localhost:8000/products')
    #    self.assertIn('Product', driver.title)

    #def testStorePage(self):
    #    driver = self.driver
    #    driver.get('http://localhost:8000/stores')
    #    self.assertIn('Store', driver.title)

    def tearDown(self):
        self.driver.close()

if __name__ == '__main__':
    unittest.main()
