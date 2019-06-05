# /urs/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import stat
import shutil
import urllib2
import requests
import zipfile

edk2platformurl="https://github.com/tianocore/edk2-platforms.git -b devel-IntelAtomProcessorE3900"
edk2url=r"-b vUDK2018 https://github.com/tianocore/edk2.git"
binaryurl="https://firmware.intel.com/sites/default/files/intelatome3900-0.71-binary.objects.zip"
fspurl="https://github.com/IntelFsp/FSP.git"
root_path=os.getcwd()
edk2path=os.path.join(root_path,"edk2")
edk2platformpath=os.path.join(root_path,"edk2-platforms")
fspdownloadpath=os.path.join(root_path,"FSP")
fsp_path=os.path.join(edk2platformpath,"Silicon\\BroxtonSoC\\BroxtonFspPkg")


class BasicFunctionLib:
    "This class mainly provides all individal function"
    def __init__(self):
        pass

    # Use request mode to download file
    def rfiles(self,url,name,attr="zip"):
        f=requests.get(url)
        filename=str(name+"."+attr)
        with open(filename,"wb") as code:
            code.write(f.content)
        code.close()
    # Use urllib2 method to download file
    def u2files(self,url,name,attr="zip"):
        req = urllib2.Request(url)
        f = urllib2.urlopen(req)
        filename = str(name + "." + attr)
        with open(filename, "wb") as code:
            code.write(f.read())
        code.close()

    def filezip(self):
        file_zip = zipfile.ZipFile("binary", 'w', zipfile.ZIP_DEFLATED)
        file_zip.write(filename, file_url)
        file_zip.close()

    def fileextract(self,name):
        file_zip = zipfile.ZipFile(name, 'r')
        for file in file_zip.namelist():
            file_zip.extract(file, "binary")
        file_zip.close()
        os.remove(name)

    def binarycp(self,filename,targetpath):
        binarypath = os.path.join(root_path, "binary")
        sourcepath = os.path.join(binarypath, filename)
        if True:
            subprocess.check_call("xcopy /E /Y %s %s" % (sourcepath, targetpath), shell=True)
        shutil.rmtree(binarypath)

    def systemdetect(self):
        if sys.platform=="win32":
            return "windows"
        elif sys.platform=="linux":
            return "linux"
        else:
            print "Please switch the build environmnt to linux or windows system"
            raise Exception("Not support this system")

    def delete_file(self):
        for edkpath in (edk2path,edk2platformpath):
            if os.path.exists(edkpath):
                for path,dirs,names in os.walk(edkpath):
                    for eachname in names:
                        absolutepath=os.path.join(path,eachname)
                        if self.systemkey=="windows":
                            os.chmod(absolutepath,stat.S_IWRITE)
                            os.remove(absolutepath)
                        else:
                            os.chmod(absolutepath, stat.S_IRWXU)
                            os.remove(absolutepath)
                shutil.rmtree(edkpath)

    def maingitclone(self):
        self.systemkey = self.systemdetect()
        self.delete_file()
        for downloadmeter in (edk2url,edk2platformurl,fspurl):
            self.checkcode = 1
            while self.checkcode:
                self.checkcode = subprocess.check_call("git clone --depth=1 %s" %downloadmeter)
        shutil.copytree(os.path.join(fspdownloadpath,"ApolloLakeFspBinPkg"),os.path.join(fsp_path,"ApolloLakeFspBinPkg"))
        if os.path.exists(fspdownloadpath):
            for path, dirs, names in os.walk(fspdownloadpath):
                for eachname in names:
                    absolutepath = os.path.join(path, eachname)
                    if self.systemkey == "windows":
                        os.chmod(absolutepath, stat.S_IWRITE)
                        os.remove(absolutepath)
                    else:
                        os.chmod(absolutepath, stat.S_IRWXU)
                        os.remove(absolutepath)
            shutil.rmtree(fspdownloadpath)

def main():
    buildbasic=BasicFunctionLib()
    buildbasic.u2files(binaryurl,"test")
    buildbasic.fileextract("test.zip")
    buildbasic.binarycp("IntelAtomE3900-0.71-Binary.Objects",edk2platformpath)

if __name__=="__main__":
    main()