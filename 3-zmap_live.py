#!/usr/bin/env python
# -*- coding:utf-8 -*-
# mail:nudtcat@gmail.com

"""

"""

import commands
import logging
import os
import argparse
import sys

logging.basicConfig(
	level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s', filename='./log/zmap_live.log'
)


class zmap_live():
	def __init__(self, filename,result_file,times):
		self.filename = filename
		self.subfile = []
		self.times=times
		self.result_file=result_file
		self.subfile_name = self.filename + "_in_"
		self.pre="res_"
		logging.info("Init finished!")

	def divide_file(self):
		cmd = "split -100 " + self.filename + " " + self.subfile_name
		if (commands.getstatusoutput(cmd)[0] == 0):
			for file in os.listdir("."):
				if self.subfile_name in file:
					self.subfile.append(file)
		logging.info("Divide file finished!")

	def zmap_scan(self):
		for file in self.subfile:
			cmd = "zmap --probe-module=icmp_echoscan --max-sendto-failures 1000000 -T 1 -b black_list.conf -f 'saddr' -w %s  -o %s"%(file,self.pre+file)
			flag=1
			for i in range(self.times):
				if(commands.getstatusoutput(cmd)[0]==0):
					flag=0
					break
			if(flag==1):
				logging.error("File %s is not finished,cmd:%s"%(file,cmd))
				print "File %s is not finished,cmd:%s"%(file,cmd)
			logging.info("Zamp scanned file %s"%(file))
		logging.info("Zmap scan finished!")

	def clean(self):
		with open(self.result_file,"w") as res_file:
			for file in self.subfile:
				os.remove(file)
				with open(self.pre+file,"r") as f:
					for line in f:
						res_file.write(line)
				os.remove(self.pre+file)
		logging.info("Clean finished!")

	def run(self):
		self.divide_file()
		self.zmap_scan()
		self.clean()


if __name__=="__main__":
	parser=argparse.ArgumentParser(
		description="Zmap_live V1.0 to scan for live hosts"
	)
	parser.add_argument("-i", "--input", metavar="",
						help="input file")
	parser.add_argument("-o", "--out", metavar="", default="./result/live_ip.txt",
					help="result out file")
	parser.add_argument("-t","--times",metavar="",default="5",
						help="Retry times in case zmap scan failed!")
	args = parser.parse_args()
	try:
		z=zmap_live(args.input,args.out,(int)(args.times))
		z.divide_file()
		print "[+]INFO:Divide file finished!"
		z.zmap_scan()
		print "[+]INFO:Scan finished"
		z.clean()
		print "[+]INFO:Results is in file %s"%(args.out)
	except KeyboardInterrupt:
		logging.info("Ctrl C - stop!")
		sys.exit(1)
