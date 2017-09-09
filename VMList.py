#!/usr/bin/env/python
import paramiko
import time
import os
import subprocess
import thread

Class VMList(threading.Thread):
	VMList[];
	Keys=['name','target_host','target_port','sshusername','sshpassword','livetime']
	def __init__(self,threadId,name,rawcomd):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.rawComd=rawComd
		
	def deleteVM(self,name):
		os.system('virsh undefined{}'.format(name))
		
	def add(self,VMname,target_host,target_port,sshusername,sshpassword):
		newVM=[VMname,taget_host,taget_port,sshusername,sshpassword,datetime.datetime.now()]
		VMList.append(dict(zip(Keys,newVM)))
		
	def run(self):
	while True:
	    time.sleep(20)
	    if list.count(VMList) >=1:
			for VM in VMList:
			  difference=getTimeDifferenceFromNow(VM['livetime'],datetime.datetime.now())
			  if difference >= 10:
				ssh.connect(VM['taget_host'],VM['target_port'],VM['sshusername'],VM['sshpassword'])
				stdin, stdout, stderr = ssh.exec_command(self.rawComd)
				line = [l for l in stdout][0].strip()
				load1, load5, load15, _, _, nb_cpus = (line.split(' '))
				load1 = float(load1)
				s_load = '%.2f' % (load1) 
				s_load = int(float(s_load))
				if s_load<=30:
					deleteVM(VM['name'])
			  
	def getTimeDifferenceFromNow(self,TimeStart, TimeEnd):
		timeDiff = TimeEnd - TimeStart
		return divmod(timeDiff.days * 86400 + timeDiff.seconds, 60)  
			
		
		
