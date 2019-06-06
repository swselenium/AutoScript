# -*- encoding:utf-8 -*-

import time
import subprocess
import unittest
from framework.browser_engine import BrowserEngine
from framework.base_page import BasePage
from framework.logger import Logger
logger=Logger("testcase-1949").getlog()

class WlanDisconnect(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        browser = BrowserEngine(cls)
        cls.driver = browser.open_browser(cls)

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()

    def test_wlan(self):
        self.initbase = BasePage(self.driver)
        self.initbase.click("l => 新闻")
        try:
            self.assertTrue("热点要闻" in self.initbase.find_element('s => a[data-control="pane-news"]').text)
        except Exception as e:
            logger.error("Fail to connect wlan: %s" %e)
            self.initbase.get_windows_screen()

    #Please update Wi-Fi by local name
    def test_wlan_Disconnect(self):
        self.initbase = BasePage(self.driver)
        subprocess.check_call("netsh interface set interface Wi-Fi disabled",shell=True)
        self.driver.get("https://wwww.baidu.com")
        try:
            self.assertTrue("No internet" in self.initbase.find_element('s => span[jsselect = "heading"]').text)
        except Exception as e:
            logger.error("Fail to disconnect wlan: %s" %e)
            self.initbase.get_windows_screen()
        finally:
            subprocess.check_call("netsh interface set interface Wi-Fi enabled", shell=True)
            time.sleep(10)

if __name__=="__main__":
    unittest.main()