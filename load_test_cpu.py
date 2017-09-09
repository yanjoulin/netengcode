#!/usr/bin/env/python
import paramiko
import time
import os
import subprocess
from VMList import *

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

target_host = '172.16.2.102'
target_port = 22
pwd = 'sandesh'
un = 'root'
stress = 'stress --cpu 100 --io 1 --vm 1 --vm-bytes 128M --timeout 120s --verbose'
raw = r"""echo "$(cat /proc/loadavg) $(grep -E '^CPU|^processor' < /proc/cpuinfo | wc -l)" """

ssh.connect( hostname = target_host , username = un, password = pwd )

print 'STRESS Command execution is in progress to increase Load ...'
print '========================================================================================'
s_load = 0

vm_list=VMList(1,"ScaledownThread",raw)
vm_list.start()
Counter=1
while s_load < 80:
	stdin, stdout, stderr = ssh.exec_command(stress)
	time.sleep(20)
	print 'Checking for Load Average ...'
	stdin, stdout, stderr = ssh.exec_command(raw)

	line = [l for l in stdout][0].strip()
	load1, load5, load15, _, _, nb_cpus = (line.split(' '))
	load1 = float(load1)
	s_load = '%.2f' % (load1)
	s_load = int(float(s_load))

	print '****************************************************************************************'
	print 'Load Average is:', s_load
	print '****************************************************************************************'

	if s_load >= 80:
		print 'Load Average Reached above 80%, spinning new VNF ... Continue with Ping Pong :-)'
		ssh.close()
		print '****************************************************************************************'
		
		Command='virt-install --name demovm{}_clone --ram 2048 --vcpus 1 --cdrom=/var/lib/libvirt/images/CentOS-7-x86_64-Minimal.iso --disk path=/var/lib/libvirt/images/centos7_1.img,size=20,bus=virtio,format=qcow2 --os-type linux --os-variant ubuntu16.04 --network=bridge=br0,model=virtio --graphics vnc --hvm --virt-type=kvm --console pty,target_type=virtio'.format(Counter)
	        os.system([Command])
		VMName='demovm{}_clone'.format(Counter)
		vm_list.add(VMName,target_host,target_port,sshusername=un,sshpassword=pwd)
		Counter+=1
	else: 
		print 'All Good, Time for Ping Pong !!!'
		print '----------------------------------------------------------------------------------------'
