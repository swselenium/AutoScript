# -*- coding:utf-8 -*-
import ConfigParser
import os,time
from selenium import webdriver
from framework.logger import Logger
logger = Logger(logger="BrowserEngine").getlog()

class BrowserEngine(object):

    def __init__(self,driver=""):
        self.driver=driver
        # self.browser_eng_dir=os.path.dirname(os.path.abspath('.'))
        # self.browser_eng_time = time.strftime("%Y-%m-%d %H_%M_%S",time.localtime())
        # self.browser_eng_name = '%s\\%s%s.png' %(self.browser_eng_dir,"logs\\Browser_eng_",self.browser_eng_time)
    # read the browser type from config.ini file, return the driver
    def open_browser(self,dr):
        self.dr=dr
        config = ConfigParser.ConfigParser()
        file_path = os.path.join(os.path.dirname(os.path.abspath('.')),'config\\config.ini')
        config.read(file_path)
        browser = config.get("browserType", "browserName")
        logger.info("You had select [%s] browser." % browser)
        url = config.get("testServer", "URL")
        logger.info("The test server url is: %s" % url)

        if browser == "Firefox":
            self.dr = webdriver.Firefox()
            logger.info("Starting Firefox browser.")
        elif browser == "Chrome":
            self.dr = webdriver.Chrome()
            logger.info("Starting Chrome browser.")
        elif browser == "IE":
            self.dr = webdriver.Ie()
            logger.info("Starting IE browser.")
        else:
            logger.error("Not support web browser")
        self.dr.get(url)
        logger.info("Open url: %s" % url)
        time.sleep(1)
        self.dr.maximize_window()
        #self.driver.save_screenshot(self.browser_eng_name)
        #info("Maximize the current window.")
        self.dr.implicitly_wait(10)
        logger.info("Set implicitly wait 10 seconds.")
        return self.dr

    def quit_browser(self):
        logger.info("Now, Close and quit the browser.")
        self.dr.quit()

if __name__=="__main__":

    test_browser_eng=BrowserEngine("test")
    test_browser_eng.open_browser("dr")
    test_browser_eng.quit_browser()



