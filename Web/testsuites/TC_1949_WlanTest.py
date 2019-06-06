# -*- encoding:utf-8 -*-

import time
import unittest
from framework.browser_engine import BrowserEngine
from framework.base_page import BasePage
from framework.logger import Logger

logger=Logger("testcase-1949").getlog()

class WlanConnect(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        browser = BrowserEngine(cls)
        cls.driver = browser.open_browser(cls)

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()

    def test_wlan_login_fail(self):

        wlan_dict={#"miss_username":['','19911992'], "miss_password":['weix.b.sun@intel.com',''],
                   "incorrect_username":['weix.b.sun.com','19911992'], "incorrect_password":['weix.b.sun@intel.com','12345678']}
        self.initbase = BasePage(self.driver)
        for key in wlan_dict:
            self.driver.get('https://gia-captiveportal.intel.com/guest/guest_hello_c.php?mac=84:3a:4b:c8:a8:f0&_browser=1')
            self.initbase.type('s => input#ID_form80308bd3_weblogin_username',wlan_dict[key][0])
            self.initbase.type('s => input#ID_form80308bd3_weblogin_password',wlan_dict[key][1])

            js_bottom = "var q=document.documentElement.scrollTop=10000"
            self.driver.execute_script(js_bottom)
            time.sleep(1)

            self.initbase.click('s => input#ID_form80308bd3_weblogin_visitor_accept_terms')
            self.initbase.click('s => input#ID_form80308bd3_weblogin_submit')
            self.initbase.get_windows_screen()
            try:
                if key.find("username"):
                    self.assertTrue('Invalid username' in self.initbase.find_element("ERROR_form39b008c_weblogin_username").text)
                else:
                    self.assertTrue('enter a value' in self.initbase.find_element("ERROR_form39b008c_weblogin_password").text)
            except Exception as e:
                logger.error("No error message was printed: %s" %e)

    def test_wlan_login_pass(self):
        username="weix.b.sun@intel.com"
        password="19911992"
        self.initbase = BasePage(self.driver)
        self.driver.get('https://gia-captiveportal.intel.com/guest/guest_hello_c.php?mac=84:3a:4b:c8:a8:f0&_browser=1')
        self.initbase.type('s => input#ID_form80308bd3_weblogin_username',username)
        self.initbase.type('s => input#ID_form80308bd3_weblogin_password',password)

        js_bottom = "var q=document.documentElement.scrollTop=10000"
        self.driver.execute_script(js_bottom)
        time.sleep(1)

        self.initbase.click('s => input#ID_form80308bd3_weblogin_visitor_accept_terms')
        self.initbase.click('s => input#ID_form80308bd3_weblogin_submit')
        self.initbase.get_windows_screen()
        try:
            self.assertTrue('Logging in' in self.initbase.find_element("s => div#content-marker > p").text)
        except Exception as e:
            logger.error("No logging message was printed: %s" %e)
            self.initbase.get_windows_screen()

if __name__ == '__main__':
    unittest.main()