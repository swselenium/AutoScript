#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import logging
import os.path
import time

class Logger(object):

    def __init__(self, logger=__name__):
        self.logger = logging.getLogger(logger)
        log_dir = self.make_log_path(os.path.abspath('.'))
        now_time = time.strftime("%Y-%m-%d %H_%M_%S",time.localtime())
        log_name = '%s\%s.log' %(log_dir,now_time)
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(name)s - [line:%(lineno)d]%(levelname)s: %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename=log_name,
                            filemode="a")

    def getlog(self):
        return self.logger

    # def getlogger2(self,loggername=__name__):
    #     # 使用一个名字为mylogger的logger
    #     self.logger2 = logging.getLogger(loggername)
    #     # 设置logger的level为DEBUG
    #     self.logger2.setLevel(logging.INFO)
    #
    #     # 创建一个输出日志到控制台的StreamHandler
    #     stream_handler = logging.StreamHandler()
    #     #'[%(asctime)s]:[%(filename)s] - %(filename)s - %(levelname)s: %(message)s'
    #     formatter = logging.Formatter('[%(asctime)s] - %(name)s - [line:%(lineno)d]%(levelname)s: %(message)s')
    #     stream_handler.setFormatter(formatter)
    #
    #     # 给logger添加上handle
    #     self.logdir = self.make_log_path(os.getcwd())
    #     self.now_time = time.strftime("%Y-%m-%d %H_%M_%S", time.localtime())
    #     self.log_name = '%s\%s.log' %(self.logdir,self.now_time)
    #     file_handler = logging.FileHandler(self.log_name)
    #     file_handler.setFormatter(formatter)
    #
    #     self.logger2.addHandler(stream_handler)#把日志打印到控制台
    #     self.logger2.addHandler(file_handler) #把日志打印到文件
    #     return  self.logger2

    def make_log_path(self,path):
        main_path=os.path.dirname(path)
        log_path = os.path.join(main_path, "logs")
        if not os.path.isdir(log_path):
            os.mkdir(log_path)
        else:
            pass
            #print("Log path is existed")
        return log_path

if __name__=="__main__":

    log_test = Logger()
    time.sleep(1)
    log_test.logger.info("No pcd module was found")
    log_test.logger.warn("No pcd module was 2found")
    print log_test.getlog
