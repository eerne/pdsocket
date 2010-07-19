import socket, threading, time, os

# import sys
# if sys.platform == 'darwin':

PDDIR = '//Applications/Pd-0.42-5.app/Contents/Resources/bin'
# assuming we are in the same dir as pd-socket.py and pd-socket.pd
FILEDIR = os.getcwd()
PORTOUT = 3005
PORTIN = 3006

class Puredata(threading.Thread):
	def run(self):
		try:
			# os.system('cd %s && ./pd -nogui' %(PDDIR))
			# -nogui -path <path> -audiobuf <n> -nostdpath  -send \"pd dsp 1;pd dsp 0;\"
			os.system('cd %s && ./pd -stderr -nostdpath -rt %s/pd-socket.pd' %(PDDIR, FILEDIR))
			wait()
		except:
			print 'couldn\'t load Pd'
		finally:
			print 'Pd bye bye'

Puredata().start();

while 1:
	time.sleep(0.25)
	try:
		pd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		pd.connect(('localhost', PORTOUT))
		break
	except socket.error, (value, message):
		if pd:
			pd.close()
		# print 'TESTING Socket-OUT:', message

pd.send('python->pd Hello Pd;')

"""
class Listener(threading.Thread):
	def run(self):
		r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		r.bind(('localhost', PORTIN))
		r.listen(2)
		pd.send('pd pd-py-socket;')
		client_socket, address = r.accept()
		# print 'python: got a connection from ', address
		while 1:
			time.sleep(0.1)
			data = client_socket.recv(1024)
			if data:
				print "python:" , data
		r.close()

Listener().start();
"""
