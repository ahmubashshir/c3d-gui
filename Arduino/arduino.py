#!/usr/bin/env python3
import serial,time,os
class InvalidPort(Exception):
	def __init__(self,message):
		self.message = message
if os.name=='nt':
	class port(object):
		def __init__(self,port="COM1",baud=9600,stopbit=serial.STOPBITS_TWO,time=0,lt='\n'):
			self.inited=False
			try:
				self.dev=serial.Serial(port,baud,timeout=time,stopbits=stopbit)
				self.inited=True
				print("Creating")
				self.lt=lt
				self.out=''
				print(self.dev)
			except serial.serialutil.SerialException:
				raise InvalidPort(port+" not found")
		def __del__(self):
			if self.inited:
				self.dev.close()
		def sendFile(self,path):
			out=''
			while self.dev.inWaiting() > 0:
				out += self.dev.read(1).decode('utf-8')
			if out != '':
				print(out,end='')
			
			with open(path,"r") as f:
				a=f.read().splitlines()
				print(a)
				for n in a:
					cmd=bytes(n+self.lt,'utf-8')
					self.dev.write(cmd)
					out = ''
					time.sleep(1)
					while self.dev.inWaiting() > 0:
						out += self.dev.read(1).decode('utf-8')
					if out != '':
						print(out,end='')

		def send(self,*cmd):
			if cmd !=[]:
				for n in cmd:
					self.dev.write(bytes(n+self.lt,'utf-8'))
					time.sleep(1)
					while self.dev.inWaiting() > 0:
						self.out += self.dev.read(1).decode('utf-8')
		def recieve(self):
			r=(self.out + '.')[:-1]
			self.out=''
			return r
else:
	class port(object):
		def __init__(self,port="/dev/ttyUSB0",baud=9600,stopbit=serial.STOPBITS_TWO,time=0,lt='\n'):
			self.inited=False
			try:
				self.dev=serial.Serial(port,baud,timeout=time,stopbits=stopbit)
				self.inited=True
				print("Creating")
				self.lt=lt
				self.out=''
				print(self.dev)
			except serial.serialutil.SerialException:
				raise InvalidPort(port+" not found")
		def __del__(self):
			if self.inited:
				self.dev.close()
		def sendFile(self,path):
			out=''
			while self.dev.inWaiting() > 0:
				out += self.dev.read(1).decode('utf-8')
			if out != '':
				print(out,end='')
			
			with open(path,"r") as f:
				a=f.read().splitlines()
				print(a)
				for n in a:
					cmd=bytes(n+self.lt,'utf-8')
					self.dev.write(cmd)
					out = ''
					time.sleep(1)
					while self.dev.inWaiting() > 0:
						out += self.dev.read(1).decode('utf-8')
					if out != '':
						print(out,end='')

		def send(self,*cmd):
			if cmd !=[]:
				for n in cmd:
					self.dev.write(bytes(n+self.lt,'utf-8'))
					time.sleep(1)
					while self.dev.inWaiting() > 0:
						self.out += self.dev.read(1).decode('utf-8')
		def recieve(self):
			r=(self.out + '.')[:-1]
			self.out=''
			return r

if __name__=="__main__":
	import sys
	if len(sys.argv)>1:
		exe=port()
		exe.sendFile(sys.argv[1])
		
