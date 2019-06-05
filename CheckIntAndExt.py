#!/usr/bin/env python
# -*- encoding: utf-8 -*-
## @file
# The script is used to compare the files between Internal (INT) and External (EXT).
# For example, compare INT DSC and EXT DSC. If one line exists only in INT DSC,
# the it needs to be wrapped. If one line exists only in EXT DSC, this line is required
# to be copied to INT DSC. This script input is three files. The first one is internal,
# the second one is external one, the last one is the updated internal one.
#
# Copyright (c) 2019, Intel Corporation. All rights reserved.<BR>
# SPDX-License-Identifier: BSD-2-Clause-Patent
#

import re
import time
import logging
import os

path = os.getcwd()
gPcdSectionRe = re.compile('^\[Pcd.*?]$', re.UNICODE)
definesSectionRe = re.compile('^\[Defines]$', re.UNICODE)
f1path = os.path.join(path,"EXT\\StructurePcd.dsc")
f2path = os.path.join(path,"INT\\StructurePcd.dsc")
logger = logging.getLogger(__name__)

def mikefiles(path):
	mf_path=os.path.join(path,"Log")
	if not os.path.isdir(mf_path):
		os.mkdir(mf_path)
	else:
		print("Log path is existed")
	return os.path.join(mf_path,"log.txt")

class DscFileUpdate:
	def __init__(self,extfile,intfile):
		self.extfile=extfile
		self.intfile=intfile
		self.exttuple=([],{},[])
		self.inttuple=([],{},[])
		
	def contextpick(self,filename):
		self.pcdkeys=[]
		self.pcdkline=[]
		self.defheader=[]
		self.header=[]
		self.pcddict={}
		with open(filename) as f:
			self.flines=f.readlines()
			length=len(self.flines)
			for line in range(length):
				lines=self.flines[line]
				if gPcdSectionRe.match(lines) is not None:
					self.pcdkline.append(line)
					self.pcdkeys.append(lines)
				elif definesSectionRe.match(lines) is not None:
					self.defheader.append(line)
				else:
					continue
			if self.defheader!=[]:
				self.header=self.flines[self.defheader[0]:self.pcdkline[0]]
			else:
				logger.info("No defines header information")
			lengthpcd=len(self.pcdkline)
			if lengthpcd>1:
				for i in range(lengthpcd):
					kh=self.pcdkline[i]
					if i<lengthpcd-1:
						kl=self.pcdkline[i+1]
						self.pcddict[self.flines[kh]]=self.flines[kh+1:kl]
					else:
						self.pcddict[self.flines[kh]]=self.flines[kh+1:]
			elif lengthpcd==1:
				kh=self.pcdkline[0]
				self.pcddict[self.flines[kh]]=self.flines[kh+1:]
			else:
				logger.info("No pcd module was found")
			return(self.header,self.pcddict,self.pcdkeys)

	def addextdiftoint(self):
		self.extonly={}
		self.extonlydict={}
		self.extonlyvalue=[]
		self.exttuple=self.contextpick(self.extfile)
		self.inttuple=self.contextpick(self.intfile)
		ek=self.exttuple[1].keys()
		ik=self.inttuple[1].keys()
		for i in ek:
			if i in ik:
				evalue=self.exttuple[1][i]
				ivalue=self.inttuple[1][i]
				try:
					for j in evalue:
						if j not in ivalue:
							extonlyline=evalue.index(j)
							valuecache=[evalue[extonlyline-1],j]
							self.extonlyvalue.append(valuecache)
				except Exception,err:
					logger.error(err,exc_info = True)
				finally:
					if self.extonlyvalue!=[]:
						self.extonly[i]=self.extonlyvalue
						self.extonlyvalue=[]
			else:
				self.inttuple[1][i]=self.exttuple[1][i]
		eonlyk=self.extonly.keys()
		for eok in eonlyk:
			difadd=self.inttuple[1][eok]
			while self.extonly[eok]:
				for eachvalue in self.extonly[eok]:
					e0=eachvalue[0]
					e1=eachvalue[1]
					if e0 in difadd:
						eokintline=difadd.index(e0)
						try:
							difadd.insert(eokintline+1,e1)
							self.extonly[eok].remove(eachvalue)
						except Exception:
							difadd.append(e1)
							self.extonly[eok].remove(eachvalue)
					else:
						continue
		return(self.exttuple,self.inttuple)

	def addintflags(self):
		self.intonly={}
		self.intonlyvalue=[]
		self.addextdiftoint()
		begain="#\n#  Platform:InternalOnlyBegin\n#\n"
		end="#\n#  Platform:InternalOnlyEnd\n#\n"
		ek=self.exttuple[1].keys()
		ik=self.inttuple[1].keys()
		for i in ik:
			if i in ek:
				ilist=self.inttuple[1][i]
				elist=self.exttuple[1][i]
				try:
					for x in ilist:
						if x not in elist:
							self.intonlyvalue.append(x)
				except Exception,err:
					logger.error("Fail to pick up different lines:\n%s" %err,exc_info = True)
				finally:
					self.intonly[i]=self.intonlyvalue
					self.intonlyvalue=[]
			else:
				self.inttuple[1][i].insert(1,begain)
				L=len(self.inttuple[1][i])
				self.inttuple[1][i].insert(L,end)
		for j in self.intonly.keys():
			for y in self.intonly[j]:
				flags=self.inttuple[1][j]
				indf=flags.index(y)
				if indf<(len(flags)-1):
					if flags[indf-1]!=end:
						flags.insert(indf+1,end)
						flags.insert(indf,begain)
					else:
						flags.insert(indf+1,end)
						flags.pop(indf-1)
				else:
					if flags[indf-1]!=end:
						flags.append(end)
						flags.insert(indf,begain)
					else:
						flags.append(end)
						flags.pop(indf-1)
		return(self.exttuple,self.inttuple)

	def reviseintdsc(self):
		self.addintflags()
		ikeys=self.inttuple[2]
		ekeys=self.exttuple[2]
		if ikeys==ekeys:
			for i in ikeys:
				self.inttuple[0].append(i)
				self.inttuple[0].extend(self.inttuple[1][i])
		else:
			for i in ekeys:
				if i not in ikeys:
					a=ekeys.index(i)
					ikeys.insert(a,i)
				else:
					continue
			for i in ikeys:
				self.inttuple[0].append(i)
				self.inttuple[0].extend(self.inttuple[1][i])
		try:
			chgf=open(self.intfile,"w+")
			for i in self.inttuple[0]:
				chgf.write(i)
		except Exception,err:
			print err
			logger.error("Fail to save results:\n%s" %err,exc_info = True)
		finally:
			chgf.close()

def main():
	logging.basicConfig(level=logging.INFO,
						format='%(asctime)s - %(name)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s',
						datefmt='%Y-%m-%d %H:%M:%S',
						filename=mikefiles(path),
						filemode="w")
	start1=time.clock()
	step=DscFileUpdate(f1path,f2path)
	step.reviseintdsc()
	t1=(time.clock()-start1)
	print "t1 is:",t1

if __name__ == "__main__":
	main()