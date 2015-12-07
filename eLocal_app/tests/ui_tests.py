import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
# eLocal_app import utils, views

class UITest(unittest.TestCase):
        #unittest.TestCase

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_eLocal_app(self):
        driver = self.driver
        wait = WebDriverWait(self.driver, 10)
        sec = 0.5
        invalid_zipCode = ['1', '12', '123', '1234', 'a', 'aa', 'aaa', 
                            'aaaa', '@/abc', '1234@', '@1234', '!@123', '!@a12']

        storeName = ["Trader Joe's", "Walgreens", "Safeway"]
        storeName_dropdown = {0: 4, 1: 2, 2: 1}
        storeName_place = {0: " on College Ave", 1: " on Shattuck Ave", 2: " on Shattuck Place"}
        storeName_membership = {0: True, 1: True, 2: True}
        productName = {0: ["Campbell's Soup", "Ribeye Steak", "Garbanzo Beans"], 
                        1: ["Garnier's Shampoo", "Dawn Hand Soap", "Sports Sunscreen"], 
                         2: ["Aspirin", "Cough Drops", "Vicks NyQuil"]}
        productDescription = {0: ["Tomato Soup sponsored by Campbell's.", "Tender slice of beef.", "Light brown beans used mainly for soups and dips."], 
                            1: ["Grapefruit antioxidant fortifying shampoo and conditioner.", "Antibacterial hand or dishwasher soap.", "SPF of 70+, dry-touch sunscreen lotion."], 
                            2: ["Pain reliever Tablets 325 mg.", "Honey-lemon flavored, ideal for sore throat.", "Cold and flu relief liquid, original, 12 oz. 2 pk."]}
        productPrice = {0: ["1.10", "3.30", "0.50"], 
                        1: ["2.50", "2.00", "5.50"], 
                         2: ["7.80", "3.50", "8.00"]}  

        print("\ntest_HomePage\n")
        self.driver.get('http://localhost:8000')
        #self.driver.get("http://elocalshops.herokuapp.com")

        print("\ntest_Create_Account\n")
        time.sleep(3)
        inputElement_CreateUsername = driver.find_element_by_id("registerForm_input_username_0")
        inputElement_CreateUsername.send_keys("Michael")
        time.sleep(sec)
        inputElement_CreatePassword = driver.find_element_by_id("registerForm_input_password_1")
        inputElement_CreatePassword.send_keys("1234")
        time.sleep(sec)
        inputElement_CreatePasswordAgain = driver.find_element_by_id("registerForm_input_checkpw_2")
        inputElement_CreatePasswordAgain.send_keys("1234")
        time.sleep(sec)
        inputElement_Merchant = driver.find_element_by_id("registerForm_checkbox_is_staff_3")
        inputElement_Merchant.click()
        time.sleep(sec)
        inputElement_ZipCode = driver.find_element_by_id("registerForm_input_zipcode_4")
        inputElement_ZipCode.send_keys('94704')
        time.sleep(sec)
        inputElement_Radius = driver.find_element_by_id("registerForm_select_radius_5")
        inputElement_Radius.send_keys("1")
        time.sleep(sec)
        submit = driver.find_element_by_id("account_submit")
        submit.submit()
        time.sleep(5)
        try:
            driver.find_element(By.LINK_TEXT, "Logout").click()
        except NoSuchElementException:
            print("\nAlready Created Account\n")

        print("\ntest_Invalid_Zipcodes\n")
        time.sleep(2)
        for i in range(len(invalid_zipCode)):
            inputElement_LoginUsername = driver.find_element_by_id("loginForm_input_username_0")
            inputElement_LoginUsername.send_keys("Michael")
            time.sleep(sec)
            inputElement_LoginPassword = driver.find_element_by_id("loginForm_input_password_1")
            inputElement_LoginPassword.send_keys("1234")
            time.sleep(sec)
            inputElement_ZipCode = driver.find_element_by_id("loginForm_input_zipcode_2")
            inputElement_ZipCode.send_keys(invalid_zipCode[i])
            time.sleep(sec)
            inputElement_Radius = driver.find_element_by_id("loginForm_select_radius_3")
            inputElement_Radius.send_keys("1")
            time.sleep(sec)
            submit = driver.find_element_by_id("login_submit")
            submit.submit()
            time.sleep(1)

        inputElement_LoginUsername = driver.find_element_by_id("loginForm_input_username_0")
        inputElement_LoginUsername.send_keys("Michael")
        time.sleep(sec)
        inputElement_LoginPassword = driver.find_element_by_id("loginForm_input_password_1")
        inputElement_LoginPassword.send_keys("1234")
        time.sleep(sec)
        inputElement_ZipCode = driver.find_element_by_id("loginForm_input_zipcode_2")
        inputElement_ZipCode.send_keys("94704")
        time.sleep(sec)
        inputElement_Radius = driver.find_element_by_id("loginForm_select_radius_3")
        inputElement_Radius.send_keys("1")
        time.sleep(sec)
        submit = driver.find_element_by_id("login_submit")
        submit.submit()
        time.sleep(1)

        driver.find_element(By.LINK_TEXT, "Merchant").click()


        print("\ntest_Add_Stores\n")
        #driver.implicitly_wait(3)
        time.sleep(5)
        for i in range(len(storeName)):
            input_storeAddress = driver.find_element_by_id("store_address")
            try:
                driver.find_element(By.LINK_TEXT, storeName[i]+storeName_place[i])
            except NoSuchElementException:
                input_storeAddress.send_keys(storeName[i])
                time.sleep(2)
                for num in range(storeName_dropdown[i]):
                    input_storeAddress.send_keys(Keys.ARROW_DOWN)
                    time.sleep(sec)
                input_storeAddress.send_keys(Keys.ENTER)
                time.sleep(sec)
                input_storeName = driver.find_element_by_id("store_name")
                input_storeName.send_keys(storeName_place[i])
                time.sleep(sec)
                membership_card = driver.find_element_by_id("has_card")
                if storeName_membership[i]:
                    membership_card.click()
                time.sleep(sec)
                submit = driver.find_element_by_id("addStore_submit")
                submit.click()
                time.sleep(5)
                continue
            print("\nAlready Created " + storeName[i]+storeName_place[i])

        print("\ntest_Add_Products\n")     

        for i in range(len(storeName)):
            time.sleep(sec)
            driver.find_element(By.LINK_TEXT, storeName[i]+storeName_place[i]).click()
            time.sleep(1)
            for j in range(len(productName[i])):
                input_productName = driver.find_element_by_id("addProduct_name")
                try:
                    driver.find_element(By.LINK_TEXT, productName[i][j])
                except NoSuchElementException:
                    input_productName.send_keys(productName[i][j])
                    time.sleep(sec)
                    input_productDescription = driver.find_element_by_id("addProduct_description")
                    input_productDescription.send_keys(productDescription[i][j])
                    time.sleep(sec)
                    input_productPrice = driver.find_element_by_id("addProduct_price")
                    input_productPrice.send_keys(productPrice[i][j])
                    time.sleep(sec)
                    submit = driver.find_element_by_id("addProduct_submit")
                    submit.click()
                    time.sleep(sec)
                    continue
                print("\nAlready Created " + productName[i][j])
            driver.find_element(By.LINK_TEXT, "Merchant").click()

        print("\ntest_Edit_Products\n") 
        editDescription = [" Espanol: Sopa de tomate patrocinado por Campbell.", 
                            " Espanol: Rebanada de licitación de carne de vacuno.",
                            " Espanol: Habas marrones claros utilizan principalmente para sopas y salsas.",]
        editPrice = ['11.10', '33.30', '5.50']
        driver.find_element(By.LINK_TEXT, storeName[0]+storeName_place[0]).click()
        for i in range(len(productName[0])):
            time.sleep(sec)
            driver.find_element(By.LINK_TEXT, productName[0][i]).click()
            time.sleep(3)
            edit_productPrice = driver.find_element_by_id("productEditForm_textarea_description_1")
            edit_productPrice.send_keys(editDescription[i])
            time.sleep(sec)
            edit_productPrice = driver.find_element_by_id("productEditForm_input_price_2")
            edit_productPrice.clear()
            edit_productPrice.send_keys(editPrice[i])
            time.sleep(sec)
            submit = driver.find_element_by_id("editProduct_submit")
            submit.click()
            time.sleep(sec)

        print("\ntest_Delete_Products\n")  
        delete_product = driver.find_element_by_id("deleteProduct")
        delete_product.click()
        time.sleep(sec)


        print("\ntest_AddCart\n")
        time.sleep(1)
        driver.find_element(By.LINK_TEXT, "Products").click()
        time.sleep(sec)
        driver.find_element(By.PARTIAL_LINK_TEXT, "Add").click()
        time.sleep(2)
        driver.find_element_by_id("cart").click()
        time.sleep(2)
        select_travel = driver.find_element_by_id("travel_mode")
        select_travel.click()
        time.sleep(sec)
        select_travel.send_keys(Keys.ARROW_DOWN)
        time.sleep(sec)
        select_travel.send_keys(Keys.ENTER)
        time.sleep(sec)
        input_startAddress = driver.find_element_by_id("start_address")
        input_startAddress.send_keys("UC Berkeley")
        time.sleep(sec)
        input_startAddress.send_keys(Keys.ARROW_DOWN)
        time.sleep(sec)
        input_startAddress.send_keys(Keys.ENTER)
        time.sleep(sec)
        input_endAddress = driver.find_element_by_id("end_address")
        input_endAddress.send_keys("Trader Joe's")
        time.sleep(sec)
        input_endAddress.send_keys(Keys.ARROW_DOWN)
        time.sleep(sec)
        input_endAddress.send_keys(Keys.ARROW_DOWN)
        time.sleep(sec)
        input_endAddress.send_keys(Keys.ARROW_DOWN)
        time.sleep(sec)
        input_endAddress.send_keys(Keys.ARROW_DOWN)
        time.sleep(sec)
        input_endAddress.send_keys(Keys.ENTER)
        time.sleep(3)
        driver.find_element_by_id("route").click()
        time.sleep(5)
        driver.find_element_by_id("removeCart").click()
        time.sleep(sec)

        print("\ntest_ProductSearch\n")
        productSearches = ['soup', 'soap', 'beans', 'garnier', 'beef', 'cold', 'sunscreen']
        driver.find_element(By.LINK_TEXT, "Products").click()
        time.sleep(sec)
        productSearch = driver.find_element_by_id("productSearch")
        for i in range(len(productSearches)):
             time.sleep(1.5)
             productSearch.send_keys(productSearches[i])
             time.sleep(1.5)
             productSearch.clear()

        print("\ntest_StoreSearch\n")
        storeSearches = ['way', 'safe', 'safeway', 'shattuck', 'joe', 'trader', 'green', 'walgreens']
        time.sleep(sec)
        driver.find_element(By.LINK_TEXT, "Stores").click()
        time.sleep(sec)
        productSearch = driver.find_element_by_id("storeSearch")
        for i in range(len(productSearches)):
             time.sleep(1.5)
             productSearch.send_keys(storeSearches[i])
             time.sleep(1.5)
             productSearch.clear()

        driver.find_element(By.LINK_TEXT, "Merchant").click()
        time.sleep(sec)

        print("\ntest_Delete_Stores\n")
        for i in range(len(storeName)):
            time.sleep(1)
            driver.find_element(By.LINK_TEXT, storeName[i]+storeName_place[i]).click()
            time.sleep(1)
            driver.find_element_by_id("delete_store").click()
            time.sleep(1)

        time.sleep(2)
        driver.find_element(By.LINK_TEXT, "Stores").click()
        time.sleep(2)
        driver.find_element(By.LINK_TEXT, "Products").click()
        time.sleep(2)


        print("\ntest_Logout\n")
        time.sleep(2)
        driver.find_element(By.LINK_TEXT, "Logout").click()

    def tearDown(self):
        time.sleep(1)
        self.driver.close()


if __name__ == '__main__':
    #unittest.main()

    suite = unittest.TestLoader().loadTestsFromTestCase(UITest)
    unittest.TextTestRunner(verbosity=2).run(suite)

