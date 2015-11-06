import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UITest(unittest.TestCase):
        #unittest.TestCase

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_eLocal_app(self):
        driver = self.driver
        wait = WebDriverWait(self.driver, 100)
        invalid_zipCode = ['1', '12', '123', '1234', 'a', 'aa', 'aaa', 'aaaa', '@/abc', '1234@', '@1234', '!@123', '!@a12']

        print("\ntest_HomePage\n")
        self.driver.get('http://localhost:8000')
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
        inputElement_Radius = driver.find_element_by_id("radius")
        inputElement_Radius.send_keys("1")
        submit = driver.find_element_by_id("submitForm")
        submit.submit()

        print("\ntest_Navbar_Add_Store\n")
        driver.find_element(By.PARTIAL_LINK_TEXT, "Add").click()
        driver.find_element(By.PARTIAL_LINK_TEXT, "Store").click()

        print("\ntest_Add_Store_Form\n")
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
       
        print("\ntest_Navbar_Add_Product\n")
        driver.find_element(By.PARTIAL_LINK_TEXT, "Add").click()
        driver.find_element(By.PARTIAL_LINK_TEXT, "Product").click()

        print("\ntest_Add_Product_Form\n")
        productName = driver.find_element_by_id("productName")
        productName.send_keys("Orange")
        productDescription = driver.find_element_by_id("description")
        productDescription.send_keys("Fruit that is a good source of vitamin C, and not to mention a very nice ingredient for orange juice.")
        productPrice = driver.find_element_by_id("productPrice")
        productPrice.send_keys("0.30")
        addProduct_submit = driver.find_element_by_id("submitAddProduct")
        addProduct_submit.click()

        print("\ntest_ProductSearch_Orange\n")
        product = driver.find_element_by_id("id_name")
        product.send_keys("orange")
        productSearch =driver.find_element_by_id("productSearch")
        productSearch.submit()

        print("\ntest_Assert_Orange_Exists\n")
        driver.find_element(By.PARTIAL_LINK_TEXT, "Orange").click()

        print("\ntest_ShoppingCart_Add_Orange\n")
        driver.find_element(By.LINK_TEXT, "Add").click()
       
        print("\ntest_ShoppingCart_Remove_Form\n")
        driver.find_element(By.PARTIAL_LINK_TEXT, "Remove").click()

        print("\ntest_Navbar_Search_Product\n")
        driver.find_element(By.PARTIAL_LINK_TEXT, "Search").click()
        driver.find_element(By.PARTIAL_LINK_TEXT, "Product").click()

        print("\ntest_Navbar_Add_Product\n")
        driver.find_element(By.PARTIAL_LINK_TEXT, "Add").click()
        driver.find_element(By.PARTIAL_LINK_TEXT, "Product").click()

        print("\ntest_Add_Product_Form\n")
        productName = driver.find_element_by_id("productName")
        productName.send_keys("Watermelon")
        productDescription = driver.find_element_by_id("description")
        productDescription.send_keys("Fruit that consists mostly of water. An ideal food in the summer and in picnics.")
        productPrice = driver.find_element_by_id("productPrice")
        productPrice.send_keys("0.50")
        addProduct_submit = driver.find_element_by_id("submitAddProduct")
        addProduct_submit.click()

        print("\ntest_ProductSearch_Watermelon\n")
        product = driver.find_element_by_id("id_name")
        product.send_keys("Watermelon")
        productSearch =driver.find_element_by_id("productSearch")
        productSearch.submit()

        print("\ntest_Assert_Watermelon_Exists\n")
        driver.find_element(By.PARTIAL_LINK_TEXT, "Watermelon").click()

        print("\ntest_Assert_Orange_NotExists\n")
        bodyText = self.driver.find_element_by_tag_name('body').text 
        self.assertNotIn('Orange', bodyText)
        #print("\ntest_EditPriceForm_Watermelon\n")
        #editPrice = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Edit")))
        #editPrice.click()

        #productName = driver.find_element_by_id("productName")
        #productName = wait.until(EC.visibility_of_element_located((By.ID, "productName")))
        #driver.implicitly_wait(3)
        #productName.send_keys("Peach")

        #updatePrice = wait.until(EC.presence_of_element_located((By.XPATH, '//button[@id="editProductPriceSubmit"]')))
        #updatePrice.submit()

        #link.click()
        #link2 = link.find_element_by_id("editProductPriceSubmit")
        #link2.click()
        #driver.implicitly_wait(10)
        #editProductPrice = driver.find_element_by_id("price")

        #editProductPrice = wait.until(EC.presence_of_element_located((By.ID, "price")))

        #driver.implicitly_wait(10)
        #editProductPrice.send_keys("1.00")
        #time.sleep(30)
        #def wait_for(condition_function):
        #    start_time = time.time()
        #    while time.time() < start_time + 3:
        #        if condition_function():
        #            return True
        #        else:
        #            time.sleep(0.1)
        #    raise Exception(
        #    'Timeout waiting for {}'.format(condition_function.__name__)
        #    )

        #def link_has_gone_stale():
        #    try:
        #        editProductPriceSubmit = driver.find_element_by_id("editProductPriceSubmit")
        #        return False
        #    except StaleElementReferenceException:
        #        return True
        #wait_for(link_has_gone_stale)
        #time.sleep(30)
        #editProductPriceSubmit = wait.until(EC.presence_of_element_located((By.ID, "editProductPriceSubmit")))
        #time.sleep(30)

        #driver.find_element(By.XPATH, '//button[@id="editProductPriceSubmit"]').click()
        #driver.implicitly_wait(10)
        #b = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="price"]')))
        #b = wait.until(EC.presence_of_element_located((By.ID, "price")))
        #driver.implicitly_wait(10)
        #b.send_keys(0.05)
        #driver.implicitly_wait(10)
        #a = wait.until(EC.presence_of_element_located((By.XPATH, '//button[@id="editProductPriceSubmit"]')))
        #a.submit()
        #editProductPriceSubmit.clickAndWait()

        #driver.find_element(By.PARTIAL_LINK_TEXT, "Update Price").click()

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
