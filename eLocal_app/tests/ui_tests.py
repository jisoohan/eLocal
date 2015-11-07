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
        #wait = WebDriverWait(self.driver, 100)
        sec = 1
        invalid_zipCode = ['1', '12', '123', '1234', 'a', 'aa', 'aaa', 'aaaa', '@/abc', '1234@', '@1234', '!@123', '!@a12']

        print("\ntest_HomePage\n")
        self.driver.get('http://localhost:8000')
        #self.driver.get("http://elocalshops.herokuapp.com")
        print("\ntest_Invalid_Zipcodes\n")
        for i in range(len(invalid_zipCode)):
            inputElement_ZipCode = driver.find_element_by_id("zip_code")
            inputElement_ZipCode.send_keys(invalid_zipCode[i])
            inputElement_Radius = driver.find_element_by_id("radius")
            inputElement_Radius.send_keys("0")
            submit = driver.find_element_by_id("submitForm")
            submit.submit()
            inputElement_ZipCode = driver.find_element_by_id("zip_code")
            inputElement_ZipCode.clear()
            bodyText = self.driver.find_element_by_tag_name('body').text 
            self.assertIn('Must be a valid zipcode', bodyText)
            print(invalid_zipCode[i] + " Yes")

        inputElement_ZipCode = driver.find_element_by_id("zip_code")
        inputElement_ZipCode.send_keys("94704")
        time.sleep(sec)
        inputElement_Radius = driver.find_element_by_id("radius")
        inputElement_Radius.send_keys("1")
        time.sleep(sec)
        submit = driver.find_element_by_id("submitForm")
        submit.submit()

        print("\ntest_Navbar_Add_Store\n")
        time.sleep(sec)
        driver.find_element(By.PARTIAL_LINK_TEXT, "Add").click()
        driver.find_element(By.PARTIAL_LINK_TEXT, "Store").click()

        print("\ntest_Add_Store_Form\n")
        driver.implicitly_wait(3)
        storeName = driver.find_element_by_id("storeName")
        storeName.send_keys("Trader's Joe")
        time.sleep(sec)
        street_number = driver.find_element_by_id("street_number")
        street_number.send_keys("1885")
        time.sleep(sec)
        address = driver.find_element_by_id("route")
        address.send_keys("University Avenue")
        time.sleep(sec)
        city = driver.find_element_by_id("locality")
        city.send_keys("Berkeley")
        time.sleep(sec)
        state = driver.find_element_by_id("administrative_area_level_1")
        state.send_keys("CA")
        time.sleep(sec)
        zipcode = driver.find_element_by_id("postal_code")
        zipcode.send_keys("94703")
        time.sleep(sec)
        country = driver.find_element_by_id("country")
        country.send_keys("US")
        time.sleep(sec)
        membership_card = driver.find_element_by_id("has_card")
        membership_card.click()
        time.sleep(sec)
        addStore_submit = driver.find_element_by_id("submitAddStore")
        addStore_submit.click()
       
        print("\ntest_Navbar_Add_Product\n")
        time.sleep(sec)
        driver.find_element(By.PARTIAL_LINK_TEXT, "Add").click()
        time.sleep(sec)
        driver.find_element(By.PARTIAL_LINK_TEXT, "Product").click()

        print("\ntest_Add_Product_Form\n")
        time.sleep(sec)
        productName = driver.find_element_by_id("productName")
        productName.send_keys("Orange")
        time.sleep(sec)
        productDescription = driver.find_element_by_id("description")
        productDescription.send_keys("Fruit that is a good source of vitamin C, and not to mention a very nice ingredient for orange juice.")
        time.sleep(sec)
        productPrice = driver.find_element_by_id("productPrice")
        productPrice.send_keys("0.30")
        time.sleep(sec)
        addProduct_submit = driver.find_element_by_id("submitAddProduct")
        addProduct_submit.click()

        print("\ntest_ProductSearch_Orange\n")
        time.sleep(sec)
        product = driver.find_element_by_id("id_name")
        product.send_keys("orange")
        time.sleep(sec)
        productSearch =driver.find_element_by_id("productSearch")
        productSearch.submit()

        print("\ntest_Assert_Orange_Exists\n")
        time.sleep(sec)
        driver.find_element(By.PARTIAL_LINK_TEXT, "Orange").click()

        print("\ntest_ShoppingCart_Add_Orange\n")
        time.sleep(sec)
        driver.find_element(By.LINK_TEXT, "Add").click()
       
        print("\ntest_ShoppingCart_Remove_Form\n")
        time.sleep(sec)
        driver.find_element(By.PARTIAL_LINK_TEXT, "Remove").click()

        print("\ntest_Navbar_Search_Product\n")
        time.sleep(sec)
        driver.find_element(By.PARTIAL_LINK_TEXT, "Search").click()
        time.sleep(sec)
        driver.find_element(By.PARTIAL_LINK_TEXT, "Product").click()

        print("\ntest_Navbar_Add_Product\n")
        time.sleep(sec)
        driver.find_element(By.PARTIAL_LINK_TEXT, "Add").click()
        time.sleep(sec)
        driver.find_element(By.PARTIAL_LINK_TEXT, "Product").click()

        print("\ntest_Add_Product_Form\n")
        time.sleep(sec)
        productName = driver.find_element_by_id("productName")
        productName.send_keys("Watermelon")
        time.sleep(sec)
        productDescription = driver.find_element_by_id("description")
        productDescription.send_keys("Fruit that consists mostly of water. An ideal food in the summer and in picnics.")
        time.sleep(sec)
        productPrice = driver.find_element_by_id("productPrice")
        productPrice.send_keys("0.50")
        time.sleep(sec)
        addProduct_submit = driver.find_element_by_id("submitAddProduct")
        addProduct_submit.click()

        print("\ntest_ProductSearch_Watermelon\n")
        time.sleep(sec)
        product = driver.find_element_by_id("id_name")
        product.send_keys("Watermelon")
        time.sleep(sec)
        productSearch =driver.find_element_by_id("productSearch")
        productSearch.submit()

        print("\ntest_Assert_Watermelon_Exists\n")
        time.sleep(sec)
        driver.find_element(By.PARTIAL_LINK_TEXT, "Watermelon").click()

        print("\ntest_Assert_Orange_NotExists\n")
        time.sleep(sec)
        driver.find_element_by_id("productClose").click()
        bodyText = self.driver.find_element_by_tag_name('body').text 
        self.assertNotIn('Orange', bodyText)
        

        print("\ntest_EditPriceForm_Watermelon\n")
        #driver.implicitly_wait(10)
        #actions = ActionChains(driver)
        #actions.move_to_element(reset)
        #actions.click_and_hold(reset)
        #actions.release(reset)
        #actions.perform()
        time.sleep(sec)
        reset = driver.find_element_by_id("productSearchReset")
        #reset = driver.find_element(By.LINK_TEXT, "Reset")
        time.sleep(sec)
        reset.click()
        #reset.click()
        time.sleep(sec)
        
        #driver.find_element(By.PARTIAL_LINK_TEXT, "Watermelon").click()
        #time.sleep(sec)
        
        
        #watermelon = driver.find_element(By.PARTIAL_LINK_TEXT, "Watermelon")
        #watermelon.click()
        #time.sleep(sec)
        #editPrice = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Edit")))
        #editPrice = driver.find_element(By.LINK_TEXT, "Edit")
        #time.sleep(sec)
        #editPrice.click()
        

        #driver.implicitly_wait(10)
        #price = driver.find_element_by_xpath('//input[@id="price"]')
        #price.send_keys("1.00")
        #updatePrice = drive.find_element_by_xpath('//button[@id="editProductPriceSubmit"]')
        #updatePrice.submit()
    
        #productName = driver.find_element_by_id("productName")
        #productName = wait.until(EC.visibility_of_element_located((By.ID, "productName")))
        #updatePrice = wait.until(EC.presence_of_element_located((By.XPATH, '//button[@id="editProductPriceSubmit"]')))
        

    #def tearDown(self):
    #    self.driver.close()


if __name__ == '__main__':
    #unittest.main()
    #unittest.main()
    #testHomePage = UITest()
    #testHomePage.setUp()
    #testHomePage.testHomePage()
    #UITest.tearDown()
    #testHomePage2 = UI2Test()
    #testHomePage2.setUp()
    #testHomePage2.testHomePage()

    suite = unittest.TestLoader().loadTestsFromTestCase(UITest)
    unittest.TextTestRunner(verbosity=2).run(suite)
