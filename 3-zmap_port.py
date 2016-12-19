#!/usr/bin/env python
#-*- coding:utf-8 -*-
#mail:nudtcat@gmail.com
"""
"""

import commands
import sys
import argparse
import logging

logging.basicConfig(
	level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s', filename='./log/zmap_port.log'
)

class zmap_port():
	def __init__(self,file,outfile,times,level):
		self.port=[21,22,23,80,443,1521,3306,3389,5900,6379,7001,8001,
				   8080,8443,554,9418,27017,27018,50060,11211,2049,25,873,3690,8888]
		self.port_service=["ftp",'ssh','telnet','http','https','oracle','mysql','mstsc','vnc','redis','weblogic','http',
						   'http','https','rtsp','git','mongodb','mongodb','hadoop','memcache','nfs','smtp','rsync','svn','http']
		self.port_level=[1,1,1,1,1,2,1,1,2,2,2,3,
						 2,2,2,3,2,2,3,2,2,3,2,3,3]
		self.file=file
		self.outfile=outfile
		self.times=times
		self.level=level
		logging.info("")

	def get_port(self):
		res=[]
		for i,l in enumerate(self.port_level):
			if l<=self.level:
				res.append(self.port[i])
		return res

	def scan(self,port_list):
		logging.info("Scan port list:%s"%(str(port_list)))
		print "[+]INFO: Scan port list:%s"%(str(port_list))
		for port in port_list:
			cmd="zmap -p %s -f 'saddr' --max-sendto-failures 10000000 -w %s -o %s_%s.txt"%(str(port),self.file,self.outfile,str(port))
			flag=1
			for i in range(self.times):
				if(commands.getstatusoutput(cmd)[0]==0):
					flag=0
					break
			if(flag==1):
				logging.error("cmd:%s is not finished!"%(cmd))
				print "[-]ERROR:cmd:%s is not finished!"%(cmd)
			else:
				logging.info("Port %s is finished!"%(str(port)))
				print "[+]INFO:Port %s is finished!"%(str(port))
		logging.info("Scan finished!")
		print "[+]INFO:Scan finished"

	def run(self):
		self.scan(self.get_port())


if __name__=="__main__":
	parser=argparse.ArgumentParser(
		description="Zmap_port V1.0 to scan for open port"
	)
	parser.add_argument("-i", "--input", metavar="",
						help="input file")
	parser.add_argument("-o", "--out", metavar="", default="port_res",
						help="result out file")
	parser.add_argument("-t", "--times", metavar="", default="5",
						help="Retry times in case zmap scan failed!")
	parser.add_argument("-l","--level",metavar="",default="2",
						help="level of ports to scan,1-3,1 means the least")
	args = parser.parse_args()
	try:
		zp=zmap_port(args.input,args.out,(int)(args.times),(int)(args.level))
		zp.run()
	except KeyboardInterrupt:
		logging.info("Ctrl C - stop!")
		sys.exit(1)
