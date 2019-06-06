# -*- encoding:utf-8 -*-

import time
import sys
import unittest
from framework.browser_engine import BrowserEngine
from framework.base_page import BasePage
from framework.logger import Logger
reload(sys)
sys.setdefaultencoding('utf-8')

logger=Logger("testcase-2029").getlog()

class GrphicVideo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        browser = BrowserEngine(cls)
        cls.driver = browser.open_browser(cls)

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()

    def test_graphic_videoplay(self):

        self.initbase = BasePage(self.driver)
        self.driver.get("https://www.iqiyi.com/v_19rsjaio7k.html")
        time.sleep(10)
        try:
            self.assertTrue("神话" in self.initbase.find_element("s => span.header-link").text)
        except Exception as e:
            logger.error("Fail to play video: %s" % e)
            self.initbase.get_windows_screen()

    def test_graphic_muiscplay(self):

        self.initbase = BasePage(self.driver)
        self.driver.get("https://www.kugou.com/song/#hash=BE6372BA684D2B195FEB691FD8DFC6CC&album_id=528482")
        self.initbase.click('toggle')
        time.sleep(10)
        try:
            self.assertTrue("Five Hundred Miles" in self.initbase.find_element("c => audioName").text)
        except Exception as e:
            logger.error("Fail to play music: %s" % e)
            self.initbase.get_windows_screen()

if __name__ == '__main__':
    unittest.main()