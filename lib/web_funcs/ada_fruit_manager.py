# local imports
from lib.funcs import *
from lib.config import config
from lib.web_funcs.parser_manager import ParserManager
# selenium imports
from selenium.webdriver.common.by import By
from selenium.webdriver.remote import webelement
# other imports
import time, pyotp



class AdaFruitManager:
    """
    Purpose - Manages web element interactions on Ada Fruit site
    """
    def __init__(self, os_type:str, testing_state:bool) -> None:
        # os type windows linux etc
        self.os_type = os_type
        # determines if program is in testing state
        self.testing_state = testing_state
        # option list
        self.parser_options = ['--start-maximized','--window-size=1920,1080','--headless']
        # if windows is os type
        if self.os_type == 'windows':
            self.parser_options = ['--start-maximized']
        # web parser object
        self.parser = ParserManager(self.os_type, config['selenium']['driver_path'],config['selenium']['url'], self.parser_options)
        # current account
        self.account_name = list(config['ada_fruit_accounts'].keys())[0]
        self.account_info = config['ada_fruit_accounts'][self.account_name]
        # type of shipping
        self.shipping_type = 'cheapest'
        # set if the bot is logged in to ada fruit
        self.logged_in = False
        # if cart is cleared
        self.cart_cleared = False
        # switch account
        self.switch_account('arwelsh')
        print(self.account_info)


    """ ------------------------------------------ Account Methods ------------------------------------------------ """
    def switch_account(self,name_of_account:str=None) -> None:
        """
        Purpose - Switchs account name and info for Ada Fruit

        Param - name_of_account: Name of the account the bot will switch to
        """
        # if a name of an account is given
        if name_of_account:
            # new account name
            self.account_name = name_of_account
        # if a name of an account is not given
        else:
            # pick the next account in the dict
            try:
                self.account_name = list(config['ada_fruit_accounts'].keys())[list(config['ada_fruit_accounts'].keys()).index(self.account_name)+1]
            # if bot is using the last account
            except IndexError:
                print("The bot is using {self.account_name} which is the last account in the dict!!!\nPlease choose a different account.\n")
        # set account info
        self.account_info = config['ada_fruit_accounts'][self.account_name]
        # set cart cleared to false
        self.cart_cleared = False


    """ ------------------------------------------ Purchase Methods ------------------------------------------------ """
    def ada_fruit_purchase(self) -> bool:
        """
        Purpose - Attempts to complete a successful transaction returns true if transaction was successful
        """
        # attempt to sign in
        self.sign_in()
        # clear cart of any items
        self.clear_cart()
        # cart prompt 
        print('\nWaiting for Item......\n')
        # iterate through product variants and waits for add to cart element
        if self.check_for_product_variants():
            # checkout prompt 
            print('\nChecking Out......')
            # start checkout process
            self.checkout()
            # refresh default page
            print('\nRefreshing Page...')
            self.parser.refresh_page()
            # purchase prompt 
            print('\nPurchased Item!')
            # sign out
            self.sign_out()
            # switch account 
            self.switch_account('artic')
            return True
        # if not product has stock
        else:
            # refresh default page
            print('\nRefreshing Page...')
            self.parser.refresh_page()
            return False


    """ ------------------------------------------ Sign In Methods ------------------------------------------------ """
    def otp_auth(self) -> None:
        """
        Purpose - Authenticates through two factor
        """
        try:
            # 2fa prompt 
            print('\nGet 2FA Token......')
            # get the token from authenticator and change otp to current 2fa
            totp = pyotp.TOTP(self.account_info['login_info']['otp'])
            token = totp.now()
            # get otp element
            opt_field = self.parser.wait_for_element(By.XPATH,'//*[@id="user_otp_attempt"]')
            # make sure element is clear of text before inputing
            opt_field.clear()
            # send info
            opt_field.send_keys(token)
            # get and click verify button element
            self.parser.click_element(self.parser.wait_for_element(By.XPATH,'//*[@id="edit_user"]/p[2]/input'))
            # check if verfication button press worked
            if self.parser.wait_for_element(By.CLASS_NAME,'alert.alert-danger.alert-dismissable',timer=1):
                # OTP prompt
                print('\nOTP Error - Retrying......')
                # hard reset page
                self.parser.hard_reset()
                # attempt to try again
                self.sign_in()
            # if black screen
            elif self.parser.wait_for_element(By.XPATH,'/html/body',timer=1).text.lower().strip() == 'Retry later'.lower():
                # OTP prompt
                print('\nBlack Screen Error - Retrying......')
                # hard reset page
                self.parser.hard_reset()
                # attempt to try again
                self.sign_in()

        # if black screen before OPT
        except Exception as e:
            # if black screen
            if self.parser.wait_for_element(By.XPATH,'/html/body',timer=1).text.lower().strip() == 'Retry later'.lower():
                # OTP prompt
                print('\nBlack Screen Error - Retrying......')
                # hard reset page
                self.parser.hard_reset()
                # attempt to try again
                self.sign_in()
            else:
                raise(e)


    def sign_in(self) -> None:
        """
        Purpose - Attempts to sign in from default ada fruit page using config file
        """
        # check if acoount had been logged in or not
        if not self.logged_in:
            # sign in prompt 
            print('\nSigning In......')
            # xpaths for username, password, and otp fields also xpath for sign in button
            xpath_dict = {'sign_in_1':'//*[@id="nav_account"]/span',
            'username':'//*[@id="user_login"]',
            'password':'//*[@id="user_password"]'}
            # if sign in button is present excute sign and 2fa
            self.parser.xpath_dict_itr(xpath_dict,self.account_info['login_info'])
            # handle captcha
            # time.sleep(6)
            # click second sign in button
            self.parser.click_element(self.parser.wait_for_element(By.XPATH,'//*[@id="new_user"]/p[3]/input'))
            # opt auth
            self.otp_auth()
            # set to logged in
            self.logged_in = True
            # sign in success prompt 
            print('\nSign In Successful!')

    def sign_out(self) -> None:
        """
        Purpose - Attempts to sign out of current account
        """
        # account dropdown element
        account_dropdown = self.parser.wait_for_element(By.CLASS_NAME,'account-dropdown.dropdown')
        # click account dropdown
        self.parser.click_element(account_dropdown)
        # dropdown container element
        dropdown_container = self.parser.wait_for_element(By.CLASS_NAME,'dropdown-container',element=account_dropdown)
        # href list
        dropdown_elements = self.parser.wait_for_elements(By.TAG_NAME,'li',element=dropdown_container)
        # iterate through href list
        for href in dropdown_elements:
            # get tag 'a' element
            a_tag_element = self.parser.wait_for_element(By.TAG_NAME,'a',element=href)
            # if the tags a elements innerhtml is 'sign out'
            if a_tag_element.get_attribute('innerHTML').lower().strip() == 'Sign Out'.lower():
                # click sign out button
                self.parser.click_element(a_tag_element)
        # refresh default page
        self.parser.refresh_page()
        # set to logged out
        self.logged_in = False
        # sign out success prompt 
        print('\nSign Out Successful!')


    """ ------------------------------------------ Product Methods ------------------------------------------------ """
    def check_for_product_variants(self) -> bool:
        """
        Purpose - Checks if product is in stock if it is returns true
        """
        # iterate through variants
        for product in self.get_products():
            # attempt to click product variant
            self.parser.click_element(product)
            # cart item
            self.cart_item()
            # item in cart
            return True
        # if cart item was not present
        return False

    def get_products(self) -> list:
        """
        Purpose - Gets all products on page and returns them in a list of web elements
        """
        # products elements to check for stock
        products = []
        # product type that is valid and needs to filter
        valid_product_type = ['2gb','4gb','8gb']
        # if testing state is true
        if self.testing_state:
            valid_product_type = ['PCB Antenna - Stacking Headers'.lower()]
        # out of stock indication
        ots_string = 'Out of stock'.lower()
        # meta options
        product_right_side = self.parser.wait_for_element(By.ID,'prod-right-side')
        # all meta options
        all_products = self.parser.wait_for_elements(By.CLASS_NAME,'top_10enabled ',element=product_right_side)
        # iterate through all meta products
        for product in all_products:
            # inner meta option name and stock status
            product_type = self.parser.wait_for_element(By.CLASS_NAME,'option_name',element=product)
            product_stock = self.parser.wait_for_element(By.CLASS_NAME,'option_meta',element=product)
            # if element equals exists
            if product_type and product_stock:
                # if testing state is true
                if self.testing_state:
                    print(product_type.get_attribute('innerHTML').lower().strip())
                    print(product_stock.get_attribute('innerHTML').lower().strip())
                # if text of element is a vaild product type 
                if product_type.get_attribute('innerHTML').lower().strip() in valid_product_type:
                    # if the product is in stock
                    if ots_string != product_stock.get_attribute('innerHTML').lower().strip():
                        # add element to product list
                        products.append(product)
                        # stock prompt 
                        print(f"\nRaspi {product_type.get_attribute('innerHTML').lower().strip()} model is in stock :)")
                    else:
                        # prompt for out of stock
                        print(f"Raspi {product_type.get_attribute('innerHTML').lower().strip()} model is out of stock :(")
            # if element equals false
            else:
                print('Warning element was not used - False.')
        # return products
        return products


    """ ------------------------------------------ Cart Methods ------------------------------------------------ """
    def clear_cart(self) -> None:
        """
        Purpose - Clears all items from cart
        """
        if not self.cart_cleared:
            # cart prompt
            print('\nClearing Cart.......')
            # get cart button
            cart_button = self.parser.wait_for_element(By.CLASS_NAME,'cart')
            # get cart count
            cart_count = self.parser.wait_for_element(By.CLASS_NAME,'cart-count',element=cart_button).text
            # if cart count is greater than 0
            if int(cart_count) > 0:
                # click cart button
                self.parser.click_element(cart_button)
                # get and click delete from cart buttons
                self.parser.click_elements(self.parser.wait_for_elements(By.CLASS_NAME,'cart-fake-button'))
                # delay
                time.sleep(1)
                # refresh default page
                self.parser.refresh_page()
            # set cart cleared
            self.cart_cleared = True
            # cart prompt
            print('\nCart Cleared!')
        
    def cart_item(self) -> None:
        """
        Purpose - Carts a specfic item on ada fruit
        """
        # get product stock right side element
        product_right_side = self.parser.wait_for_element(By.ID,'prod-right-side')
        # get and click add to cart button
        self.parser.click_element(self.parser.wait_for_element(By.XPATH,'//*[@id="prod-add-btn"]', element=product_right_side))
        # get and click my cart button
        self.parser.click_element(self.parser.wait_for_element(By.XPATH,'//*[@id="nav_account"]/div'))
        # get and click checkout button
        self.parser.click_element(self.parser.wait_for_element(By.CLASS_NAME,'mobile-button-row'))


    """ ------------------------------------------ Shipping Methods ------------------------------------------------ """
    def determine_shipping(self) -> webelement:
        """
        Purpose - Determines shipping type at checkout and returns the radio button web element of that shipping type
        """
        # get shipping types by label
        shipping_label_elements = self.parser.wait_for_elements(By.CLASS_NAME,'checkboxLabel.sg-label.checkout-shipping-method-label')
        print(shipping_label_elements)
        # if shipping type is select for the cheapest or expensive option
        if self.shipping_type in ['cheapest','expensive']:
            # if shipping type is the cheapest option
            if self.shipping_type == 'cheapest':
                # get shipping type
                return min(shipping_label_elements, key=lambda shipping_label_element: float(shipping_label_element.text.split(':')[-1].replace('$','')))
            # if shipping type is the expensive option
            elif self.shipping_type == 'expensive':
                # get shipping type
                return max(shipping_label_elements, key=lambda shipping_label_element: float(shipping_label_element.text.split(':')[-1].replace('$','')))
        # if shipping type is by name or null
        else:
            # get shipping type
            shipping_label_element = list(filter(lambda shipping_label_element: self.shipping_type.lower() in shipping_label_element.get_attribute('for').lower(), shipping_label_elements))
            # if label is found
            if shipping_label_element:
                return shipping_label_element[0]
            # if label is not found
            else:
                # prompt
                print(f'The shipping type recorded: {self.shipping_type.lower()} was not found as a shipping option.\nShipping options are changed based on number of products at checkout.')
                print(f'The cheapest shipping method will be selected instead.')
                return min(shipping_label_elements, key=lambda shipping_label_element: float(shipping_label_element.text.split(':')[-1].replace('$','')))


    """ ------------------------------------------ Checkout Methods ------------------------------------------------ """
    def checkout(self) -> None:
        """
        Purpose - Interacts with a series of checkout element to complete an order 
        """
        # xpaths for shipping info
        xpath_dict = {
        'name':'//*[@id="delivery_name"]',
        'address':'//*[@id="delivery_address1"]',
        'additional_address':'//*[@id="delivery_address2"]',
        'city':'//*[@id="delivery_city"]', 
        'state':'//*[@id="delivery_state_dropdown"]',
        'postal_code':'//*[@id="delivery_postcode"]',
        'phone_number':'//*[@id="delivery_phone"]'}
        # start shipping process
        self.parser.xpath_dict_itr(xpath_dict,self.account_info['checkout_info'])
        # get and click save and contiune button
        self.parser.click_element(self.parser.wait_for_element(By.CLASS_NAME,'blue-button.sg-button.savecontinueblue'))
        # check if address is valid
        next_continue_button = self.parser.wait_for_element(By.CLASS_NAME,'blue-button.sg-button.savecontinueblue')
        print(next_continue_button.text.lower().strip())
        # if the next continue button is for address click
        if next_continue_button.text.lower().strip() == 'Use Address as Entered'.lower():
            self.parser.click_element(next_continue_button)
        # get and click shipping option
        self.parser.click_element(self.determine_shipping())
        # get and click save and contiune button
        self.parser.click_element(self.parser.wait_for_element(By.CLASS_NAME,'blue-button.sg-button.savecontinueblue'))
        # get and click save and contiune button
        self.parser.click_element(self.parser.wait_for_element(By.CLASS_NAME,'blue-button.sg-button.savecontinueblue'))\
        # get and click save and submit button
        submit_button = self.parser.wait_for_element(By.CLASS_NAME,'sg-button.green-button.bold.submitOrder')
        if self.testing_state == False:
            self.parser.click_element(submit_button)
        # sleep for a sec
        time.sleep(.5)

