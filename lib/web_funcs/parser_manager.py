# local imports
from lib.funcs import *
# selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, ElementNotInteractableException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote import webelement
# other imports
import time

# set options
OPTIONS = webdriver.ChromeOptions()

class ParserManager:
    """
    Purpose - A web parser object that uses selenium to guide certain web element behaviors
    """
    def __init__(self, os_type:str, driver_path:str, product_url:str, options=[]) -> None:
        # os type windows linux etc
        self.os_type = os_type
        # driver path
        self.driver_path = driver_path
        # product url
        self.product_url = product_url
        # add options
        [self.add_option(option) for option in options]
        # web driver
        self.driver = webdriver.Chrome(convert_path_os('/usr/lib/chromium-browser/chromedriver'),options=OPTIONS) if self.os_type == 'linux' else webdriver.Chrome(convert_path_os(self.driver_path),options=OPTIONS)
        # set web driver to product link
        self.set_page(self.product_url)


    """ ------------------------------------------ General Methods ------------------------------------------------ """
    def set_page(self, new_link:str) -> None:
        """
        Purpose - Sets the drivers html site

        Param - new_link: The new link that the driver will be set to
        """
        self.link = new_link
        self.driver.get(self.link)

    def hard_reset(self):
        """
        Purpose - Hard reset page
        """
        # hard reset prompt
        print('\nReseting......')
        # dispose driver
        self.driver.quit()
        # reassign driver
        self.driver = webdriver.Chrome(convert_path_os('/usr/lib/chromium-browser/chromedriver'),options=OPTIONS) if self.os_type == 'linux' else webdriver.Chrome(convert_path_os(self.driver_path),options=OPTIONS)
        # set web driver to product link
        self.set_page(self.product_url)


    def refresh_page(self) -> None:
        """
        Purpose - Refreshes the page based on the current link
        """
        self.driver.get(self.link)

    def add_option(self,option=str) -> None:
        """
        Purpose - Adds an arguement to the option object

        Param - option: The option that will be added to the webdriver
        """        
        OPTIONS.add_argument(option)


    """ ------------------------------------------ Locator Methods ------------------------------------------------ """
    def find_element_by_name(self, name:str) -> webelement:
        """
        Purpose - Finds an element by the name locator

        Param - name: The name that is used to search for element
        """
        return self.driver.find_element(By.NAME, name)
        
    def find_element_by_xpath(self, xpath:str) -> webelement:
        """
        Purpose - Finds an element by the xpath locator

        Param - name: The xpath that is used to search for element
        """
        return self.driver.find_element(By.XPATH, xpath)
    
    def find_element_by_id(self, element_id:str) -> webelement:
        """
        Purpose - Finds an element by the id locator

        Param - name: The id that is used to search for element
        """
        return self.driver.find_element(By.ID, element_id)

    def find_element_by_class(self, class_name:str) -> webelement:
        """
        Purpose - Finds an element by the class name locator

        Param - name: The class name that is used to search for element
        """
        return self.driver.find_element(By.CLASS_NAME, class_name)

    def find_element_by_tag(self, tag_name:str) -> webelement:
        """
        Purpose - Finds an element by the tag name locator

        Param - name: The tag name that is used to search for element
        """
        return self.driver.find_element(By.TAG_NAME, tag_name)

    def find_element_by_css(self, css_selector:str) -> webelement:
        """
        Purpose - Finds an element by the css selector locator

        Param - name: The css selector that is used to search for element
        """
        return self.driver.find_element(By.CSS_SELECTOR, css_selector)

    def find_link_by_text(self, link_text:str) -> webelement:
        """
        Purpose - Finds an element by the link text locator

        Param - name: The link text that is used to search for element
        """
        return self.driver.find_element(By.LINK_TEXT, link_text)


    """ ------------------------------------------ Wait Methods ------------------------------------------------ """
    def wait_for_element(self, search_type:str, search_str:str, element=None, timer:int=7) -> webelement:
        """
        Purpose - Waits until an element is available

        Param - search_type: The locator that is used to search for element

        Param - search_str: The string that is used to search for element

        Param - element: The element that is used to search for another element (acts as driver)

        Param - timer: The amount of time the driver will wait for an element
        """
        try:
            # if search locator is an element and not the driver
            if element:
                return WebDriverWait(element, timer).until(EC.presence_of_element_located((search_type, search_str)))
            # if search locator is the driver and not an element
            else:
                return WebDriverWait(self.driver, timer).until(EC.presence_of_element_located((search_type, search_str)))
        # handle timeout 
        except TimeoutException as e:
            return False


    def wait_for_elements(self, search_type:str, search_str:str, element=None, timer:int=7) -> webelement:
        """
        Purpose - Waits until an element is available

        Param - search_type: The locator that is used to search for element

        Param - search_str: The string that is used to search for element

        Param - element: The element that is used to search for another element (acts as driver)

        Param - timer: The amount of time the driver will wait for an element
        """
        try:
            # if search locator is an element and not the driver
            if element:
                return WebDriverWait(element, timer).until(EC.presence_of_all_elements_located((search_type, search_str)))
            # if search locator is the driver and not an element
            else:
                return WebDriverWait(self.driver, timer).until(EC.presence_of_all_elements_located((search_type, search_str)))
        # handle timeout and "The custom error module does not recognize this error."
        except TimeoutException as e:
            return False


    """ ------------------------------------------ Click Methods ------------------------------------------------ """
    def click_element(self, element:webelement) -> None:
        """
        Purpose - Clicking an web element with error handling

        Param - element: The web element to be clicked
        """
        try:
            # click element
            element.click()
            # wait
            self.driver.implicitly_wait(5)
            # return true
            return True
        except ElementNotInteractableException as e:
            print(e)
            print('''Could not click\n1. Element is not visible\n2. Element is present in off screen (After scroll down it will display)\n3. Element is present behind any other element\n4. Element is disabled''')
            print(f'element display state is {element.is_displayed()}')
            # return false
            return False
        except AttributeError as e:
            print(e)
            # return false
            return False

    def click_elements(self, element_list:list) -> None:
        """
        Purpose - Clicking multiple web elements with error handling

        Param - element_list: The list of web elements to be clicked
        """
        try:
            for element in element_list:
                # click element
                element.click()
                # wait
                self.driver.implicitly_wait(5)
            # return true
            return True
        except ElementNotInteractableException as e:
            print(e)
            print('''Could not click\n1. Element is not visible\n2. Element is present in off screen (After scroll down it will display)\n3. Element is present behind any other element\n4. Element is disabled''')
            print(f'element display state is {element.is_displayed()}')
            # return false
            return False
        except AttributeError as e:
            print(e)
            # return false
            return False


    """ ------------------------------------------ Other Methods ------------------------------------------------ """
    def xpath_dict_itr(self,xpath_dict:dict,corresponding_dict:dict={}) -> bool:
        """
        Purpose - Iterate through a dict of web element to interact consecutively, return false if the element was not available or wasnt used

        Param - xpath_dict: A dict of web elements to parse

        Param - corresponding_dict (Optional): A dict that has information for field values (rare use case).
        """
        # element
        ele = None
        # iterate through xpath dict
        for key in xpath_dict:
            # attempt to send keys / click elements
            try:
                # get element
                ele = self.wait_for_element(By.XPATH,xpath_dict[key])
                # if element is located
                if ele:
                    # check if element has a tag that allows input
                    if ele.tag_name in ['input','select'] and ele.get_attribute('type') in ['tel', 'email','text','select-one','password']:
                        # wait for autocomplete
                        time.sleep(.05)
                        # make sure element is clear of text before inputing
                        if ele.get_attribute('type') not in ['select-one']:
                            ele.clear()
                        # send info
                        ele.send_keys(corresponding_dict[key])
                    # check if element has send keys method
                    elif ele.tag_name in ['button','span'] or ele.get_attribute('type') in ['radio','submit']:
                        # click element
                        self.click_element(ele)
                    # if element was not used
                    else:
                        print('Element not avaliable')
                        return False
                else:
                    # if element equals false
                    print('Warning element was not used - False.')
                    return False
            # except any exception and print            
            except Exception as e:
                raise(e)

        # if no errors and all elements were used
        return True




