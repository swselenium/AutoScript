# coding=utf-8

import os
import unittest
import time
import sys
sys.path.append("..")
from framework.base_page import BasePage
from HTMLTestRunner import HTMLTestRunner

# make test_report dir
report_path_make = BasePage("")
report_path = report_path_make.make_file_path(os.getcwd(),"test_report")

now_time = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime())
HtmlFile = report_path + now_time + "HTMLtemplate.html"
case_path = os.path.join(os.path.abspath('.'),"testsuites\\")
result = file(HtmlFile, "wb")

discover_suite = unittest.defaultTestLoader.discover(os.getcwd(),pattern ="TC*.py",top_level_dir=None)

if __name__ =='__main__':

    runner = HTMLTestRunner(stream=result, title=u"web test report", description=u"All test case run result:")
    runner.run(discover_suite)
