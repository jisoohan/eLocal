import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

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
        #driver.get('http://localhost:8000/stores/add')
        #goToAddStoreForm = driver.find_element_by_id("StoreForm")
        #goToAddStoreForm.click()
        #driver.switch_to.window("#addStore")
        #WebDriverWait(10)
        driver.implicitly_wait(3)
        driver.find_element(By.PARTIAL_LINK_TEXT, "Add").click()
        driver.find_element(By.PARTIAL_LINK_TEXT, "Store").click()
        driver.implicitly_wait(3)
        storeName = driver.find_element_by_id("storeName")
        storeName.send_keys("Trader's Joe")
        street_number = driver.find_element_by_id("street_number")
        street_number.send_keys("1885")
        address = driver.find_element_by_id("route")
        address.send_keys("University Avenue")
        city = driver.find_element_by_id("locality")
        city.send_keys("Berkeley")
        state = driver.find_element_by_id("administrative_area_level_1")
        state.send_keys("CA")
        zipcode = driver.find_element_by_id("postal_code")
        zipcode.send_keys("94703")
        country = driver.find_element_by_id("country")
        country.send_keys("US")
        membership_card = driver.find_element_by_id("has_card")
        membership_card.click()
        addStore_submit = driver.find_element_by_id("submitAddStore")
        addStore_submit.click()

    #def tearDown(self):
    #    self.driver.close()

if __name__ == '__main__':
    unittest.main()
    #unittest.setUp()
    #UITest.testHomePage()
    #UITest.tearDown()
