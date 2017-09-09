#!/usr/bin/env/python
import paramiko
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

target_host = '192.168.68.11'
target_port = 22
pwd = 'cisco'
un = 'admin'

raw = "show int gi2 | include input\ rate"

print('STRESS Command execution is in progress to increase Load ...')
print('========================================================================================')
s_load = 0

while s_load < 100000:
    print('Checking for Load Average ...')
    ssh.connect( hostname = target_host , username = un, password = pwd )
    stdin, stdout, stderr = ssh.exec_command(raw)

    line = [l for l in stdout][0].strip()
    load1 = (line.split(' '))
    s_load = int(load1[4])
  
    print('****************************************************************************************')
    print('Load Average is:', s_load)
    print('****************************************************************************************')

    if s_load >= 80:
        print('Load Average Reached above 80%, spinning new VNF ... Continue with Ping Pong :-)')
        ssh.close()
        print('****************************************************************************************')
        #os.system('virt-install --name demovm01_clone --ram 2048 --vcpus 1 --cdrom=/var/lib/libvirt/images/CentOS-7-x86_64-Minimal.iso --disk path=/var/lib/libvirt/images/centos7_1.img,size=20,bus=virtio,format=qcow2 --os-type linux --os-variant ubuntu16.04 --network=bridge=br0,model=virtio --graphics vnc --hvm --virt-type=kvm --console pty,target_type=virtio') 
    else: 
        print('All Good, Time for Ping Pong !!!')
        print('----------------------------------------------------------------------------------------')
        
    time.sleep(3)