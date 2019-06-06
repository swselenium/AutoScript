# coding=utf-8
import os,time
from selenium.common.exceptions import NoSuchElementException
from framework.logger import Logger
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = Logger(logger="BasePage").getlog()


class BasePage(object):
    """
    For packing all base function.
    """
    def __init__(self, driver):
        self.driver = driver

    # quit browser and end testing
    def quit_browser(self):
        self.driver.quit()

    def forward(self):
        self.driver.forward()
        logger.info("Click forward on current page.")

    def back(self):
        self.driver.back()
        logger.info("Click back on current page.")

    def wait(self,seconds):
        self.driver.implicitly_wait(seconds)
        logger.info("wait for %d seconds." % seconds)

    def close(self):
        try:
            self.driver.close()
            logger.info("Closing the browser.")
        except NameError as e:
            logger.error("Failed to close the browser with %s" % e)

    def quit(self):
        try:
            self.driver.quit()
            logger.info("Quiting the browser.")
        except NameError as e:
            logger.error("Failed to quit the browser with %s" % e)

    def get_windows_screen(self):
        """
        Make screenshots dir and save the picture to here.
        """
        screen_dir=self.make_file_path(os.path.abspath('.'),"screenshots")
        screen_time = time.strftime("%Y-%m-%d %H_%M_%S",time.localtime())
        screen_name = '%s%s%s.png' %(screen_dir,"Browser_eng-",screen_time)
        try:
            self.driver.save_screenshot(screen_name)
            logger.info("Take screenshot and save to folder : /screenshots")
        except Exception as e:
            logger.error("Failed to take screenshot! %s" %e)
            self.get_windows_screen()
    def find_element(self,selector):
        """
        This mode contain all method to identify element.
        """
        element = ''
        if "=>" not in selector:
            return self.driver.find_element_by_id(selector)
        else:
            selector_by=selector.split("=>")[0].strip()
            selector_value=selector.split("=>")[1].strip()
            if selector_by=="i" or selector_by=="id":
                try:
                    element = self.driver.find_element_by_id(selector_value)
                    logger.info("Find the element \'%s\' successful by %s via value: %s " %(element.text, selector_by, selector_value))
                except NoSuchElementException as e:
                    logger.error("NoSuchElementException: %s" %e)
                    self.get_windows_screen()
            elif selector_by == "n" or selector_by == 'name':
                try:
                    element = self.driver.find_element_by_name(selector_value)
                    logger.info("Find the element \'%s\' successful by %s via value: %s " %(element.text, selector_by, selector_value))
                except NoSuchElementException as e:
                    logger.error("NoSuchElementException: %s" %e)
                    self.get_windows_screen()
            elif selector_by == "c" or selector_by == 'class_name':
                try:
                    element = self.driver.find_element_by_class_name(selector_value)
                    logger.info("Find the element \'%s\' successful by %s via value: %s " %(element.text, selector_by, selector_value))
                except NoSuchElementException as e:
                    logger.error("NoSuchElementException: %s" %e)
                    self.get_windows_screen()
            elif selector_by == "l" or selector_by == 'link_text':
                try:
                    element = self.driver.find_element_by_link_text(selector_value)
                    logger.info("Find the element \'%s\' successful by %s via value: %s " %(element.text, selector_by, selector_value))
                except NoSuchElementException as e:
                    logger.error("NoSuchElementException: %s" %e)
                    self.get_windows_screen()
            elif selector_by == "p" or selector_by == 'partial_link_text':
                try:
                    element = self.driver.find_element_by_partial_link_text(selector_value)
                    logger.info("Find the element \'%s\' successful by %s via value: %s " %(element.text, selector_by, selector_value))
                except NoSuchElementException as e:
                    logger.error("NoSuchElementException: %s" %e)
                    self.get_windows_screen()
            elif selector_by == "t" or selector_by == 'tag_name':
                try:
                    element = self.driver.find_element_by_tag_name(selector_value)
                    logger.info("Find the element \'%s\' successful by %s via value: %s " %(element.text, selector_by, selector_value))
                except NoSuchElementException as e:
                    logger.error("NoSuchElementException: %s" %e)
                    self.get_windows_screen()
            elif selector_by == "x" or selector_by == 'xpath':
                try:
                    element = self.driver.find_element_by_xpath(selector_value)
                    logger.info("Find the element \'%s\' successful by %s via value: %s " %(element.text, selector_by, selector_value))
                except NoSuchElementException as e:
                    logger.error("NoSuchElementException: %s" %e)
                    self.get_windows_screen()
            elif selector_by == "s" or selector_by == 'selector_selector':
                try:
                    element = self.driver.find_element_by_css_selector(selector_value)
                    logger.info("Find the element \'%s\' successful by %s via value: %s " %(element.text, selector_by, selector_value))
                except NoSuchElementException as e:
                    logger.error("NoSuchElementException: %s" %e)
                    self.get_windows_screen()
            else:
                raise ValueError("Please enter a valid type of targeting elements.")
        return element

    def type(self,selector,text):

        element_input = self.find_element(selector)
        element_input.clear()
        try:
            element_input.send_keys(text)
            logger.info("Type \'%s\' in input box" %text)
        except Exception as e:
            logger.error("Failed to type in input box with %s" %e)
            self.get_windows_screen()

    def clear(self, selector):

        element_clear = self.find_element(selector)
        try:
            element_clear.clear()
            logger.info("Clear input tbox before typing.")
        except Exception as e:
            logger.error("Failed to clear input box with %s" %e)
            self.get_windows_screen()

    def click(self, selector):

        element_click = self.find_element(selector)
        try:
            element_click.click()
            logger.info("The element was clicked.")
        except NameError as e:
            logger.error("Failed to click the element with %s" %e)

    def get_page_title(self):
        logger.info("Current page title is %s" % self.driver.title)
        return self.driver.title

    def make_file_path(self,path,file):
        self.main_path=os.path.dirname(path)
        self.log_path = os.path.join(self.main_path,file+"/")
        if not os.path.isdir(self.log_path):
            os.mkdir(self.log_path)
            print("make %s dir success" %file)
        else:
            print("%s dir is existed" %file)
        return self.log_path

    @staticmethod
    def sleep(seconds):
        time.sleep(seconds)
        logger.info("Sleep for %d seconds" % seconds)

