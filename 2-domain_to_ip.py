#!/usr/bin/env python
#-*- coding:utf-8 -*-
#mail:nudtcat@gmail.com

import logging
import socket
import traceback
import argparse
import sys

logging.basicConfig(
	level=logging.INFO,format='%(asctime)s [%(levelname)s] %(message)s',filename='./log/domain_to_ip.log'
)

class domain_query():
	def __init__(self,filename):
		self.ip_const=[1,256,256*256,256*256*256]
		self.domain_list=[]
		with open(filename,'r') as f:
			for line in f.readlines():
				self.domain_list.append(line.strip())
		self.ip_set=set()
		logging.info("Init finished")
		self.ip_domain_dict={}
	def query(self):
		for domain_name in self.domain_list:
			try:
				ips=set()
				for item in socket.getaddrinfo(domain_name,None):
					if len(item[-1])==2:
						ip_addr=item[-1][0]
						self.ip_set.add(ip_addr)
						ips.add(ip_addr)
				self.ip_domain_dict[domain_name]=tuple(ips)
			except :
				logging.error(traceback.format_exc())
				continue
		logging.info("Query finished")
	def get_ip(self,scope):
		logging.info(self.ip_set)
		if scope==3:
			gap=256*256
		if scope==2:
			gap=256*64
		if scope==1:
			gap=256*32
		if scope==0:
			gap=256*16
		ips=[self.ip_to_num(ip) for ip in self.ip_set]
		ips=sorted(ips)
		ip_pointer=ips[0]
		start=0
		ip_pairs=[]
		for i,ip in enumerate(ips):
			if ip>ip_pointer+gap:
				ip_pairs.append(range(ips[start]&0xffffff00,ips[i-1]+1,256))
				start=i
			if i==len(ips)-1:
				ip_pairs.append(range(ips[start]&0xffffff00,ips[i]+1,256))
			ip_pointer = ip
		res=[]
		for num_list in ip_pairs:
			for item in num_list:
				res.append(self.num_to_ip(item)+"/24")
				pass
		logging.info("Get ip address finished!")
		return res

	def get_dict(self):
		logging.info("Get dict finished!")
		return self.ip_domain_dict

	def ip_to_num(self,ip):
		num=0
		for i,item in enumerate(ip.split(".")[::-1]):
			num+=self.ip_const[i]*(int)(item)
		return num
	def num_to_ip(self,num):
		ip=[0,0,0,0]
		for i,item in enumerate(self.ip_const[::-1]):
			ip[i]=num/item
			num=num%item
		return '%s.%s.%s.%s'%(ip[0],ip[1],ip[2],ip[3])




if __name__=="__main__":
	parser=argparse.ArgumentParser(description="Domain_to_ip v1.0 to query domain name to ip address and format ip address")
	parser.add_argument("-i","--input",metavar="",
						help="input file")
	parser.add_argument("-o","--out",metavar="",default="./result/ip.txt",
						help="result out file")
	parser.add_argument("-s","--scope",metavar="",default="1",
						help="format scope,from 0 to 3,0 means a small scope")
	args=parser.parse_args()
	try:
		input_file=args.input
		output_file=args.out
		scope=(int)(args.scope)
		logging.info("start!")
		d=domain_query(input_file)
		d.query()
		print "[INFO]Query results:"
		print d.get_dict()
		print "[INFO]ip set:"
		print d.ip_set
		with open(output_file,"a") as f:
			res=d.get_ip(scope)
			for ip_seg in res:
				f.write(ip_seg+"\n")
	except KeyboardInterrupt:
		logging.info("Ctrl C - stop!")
		sys.exit(1)