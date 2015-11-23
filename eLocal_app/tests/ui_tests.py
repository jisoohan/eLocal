import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
# eLocal_app import utils, views

class UITest(unittest.TestCase):
        #unittest.TestCase

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_eLocal_app(self):
        driver = self.driver
        wait = WebDriverWait(self.driver, 10)
        sec = 0.5
        invalid_zipCode = ['1', '12', '123', '1234', 'a', 'aa', 'aaa', 'aaaa', '@/abc', '1234@', '@1234', '!@123', '!@a12']

        print("\ntest_HomePage\n")
        self.driver.get('http://localhost:8000')
        #self.driver.get("http://elocalshops.herokuapp.com")
        print("\ntest_Invalid_Zipcodes\n")
        for i in range(len(invalid_zipCode)):
            inputElement_ZipCode = driver.find_element_by_id("zipcodeForm_input_zipcode_0")
            inputElement_ZipCode.send_keys(invalid_zipCode[i])
            time.sleep(sec)
            inputElement_Radius = driver.find_element_by_id("zipcodeForm_select_radius_1")
            inputElement_Radius.send_keys("1")
            time.sleep(sec)
            submit = driver.find_element_by_id("zipcode_submit")
            submit.submit()

        inputElement_ZipCode = driver.find_element_by_id("zipcodeForm_input_zipcode_0")
        inputElement_ZipCode.send_keys("94704")
        time.sleep(sec)
        inputElement_Radius = driver.find_element_by_id("zipcodeForm_select_radius_1")
        inputElement_Radius.send_keys("0")
        time.sleep(sec)
        submit = driver.find_element_by_id("zipcode_submit")
        submit.submit()
        time.sleep(5)


        
    def tearDown(self):
        time.sleep(3)
        self.driver.close()
        


if __name__ == '__main__':
    #unittest.main()

    suite = unittest.TestLoader().loadTestsFromTestCase(UITest)
    unittest.TextTestRunner(verbosity=2).run(suite)
