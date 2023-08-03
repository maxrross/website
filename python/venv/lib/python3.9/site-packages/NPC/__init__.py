import socket
import sys
import msvcrt
import threading
import time
from flask import Flask, request
from werkzeug.utils import secure_filename
import struct
import netifaces
import requests



def addrDet(interface):
	addrs = netifaces.ifaddresses(interface)
	print(addrs[netifaces.AF_INET])

def netInfo():
	print("Interfaces")
	for net in netifaces.interfaces():
		addrDet(net)
	# print("Gateways")
	# print(netifaces.gateways())

def ntpAck(ip):
	UDP_IP = ip
	UDP_PORT = 6140
	HEX = 0x2F03F4B2
	I = 0
	V = 0
	C = 0
	PAYLOAD = struct.pack("!L3i", HEX, I, V, C)
	comsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	comsocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	comsocket.sendto(PAYLOAD, (UDP_IP, UDP_PORT))
	comsocket.settimeout(5.0)
	try:
		data, wherefrom = comsocket.recvfrom(1024, 0)
		print(data.decode())
		# print(data.decode())
		print("==> "+wherefrom[0])
	except:
		pass
	comsocket.close()

def ntpExec(message,ip,timeout_val):
		UDP_IP = ip
		UDP_PORT = 6139
		HEX = 0x2F03F4B2
		I = 0
		V = 0
		C = 0
		message+="\nsent = inbound.sendto(str(processed_data).encode(), address)"
		PAYLOAD = struct.pack("!L3i", HEX, I, V, C)
		comsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		comsocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		comsocket.sendto(message.encode(), (UDP_IP, UDP_PORT))
		comsocket.settimeout(timeout_val)
		try:
			data, wherefrom = comsocket.recvfrom(1024, 0)
			# print(data.decode(), wherefrom)
			return data
			# print(wherefrom[0])
		except:
			return -1
			pass
		comsocket.close()

def findServers():
	print('Finding for execution servers')
	print()
	for net in netifaces.interfaces():
		addrs = netifaces.ifaddresses(net)
		try:
			ntpAck(addrs[netifaces.AF_INET][0]['broadcast'])
		except:
			pass
	print()

def fileTransfer(ip, file_path): 
	#os.system("curl -i -X POST 127.0.0.1:7000/upload --upload-file centos-inital.sh")
	url = 'http://' + ip + ":"+ str(6138) + "/upload"
	files = {
		'file': open(file_path, 'rb')
	}
	r = requests.post(url, files = files)
	print(r.content.decode())


def register(ip, file_path): 
	#os.system("curl -i -X POST 127.0.0.1:7000/upload --upload-file centos-inital.sh")
	url = 'http://' + ip + ":"+ str(6138) + "/register"
	files = {
		'file': open(file_path, 'rb')
	}
	r = requests.post(url, files = files)
	print(r.content.decode())