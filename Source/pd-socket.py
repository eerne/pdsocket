import socket, threading, os, sys

class Puredata(threading.Thread):
	def prepare(self, pd = 'pd', dir = './', file = 'pd-socket.pd', args = '-stderr -nostdpath -rt -send \"pd dsp 1;pd dsp 0;\"'):
		self.pd = pd
		self.dir = dir
		self.file = file
		# args = -stderr -nostdpath -rt -nogui -path <path> -audiobuf <n> -nostdpath -nogui -send \"pd dsp 1;pd dsp 0;\"
		# note in -nogui you can't use -send
		self.args = args
		return self
	def run(self):
		try:
			os.system('cd %s && ./pd %s %s/%s' %(self.pd, self.args, self.dir, self.file))
		except:
			print 'couldn\'t load Pd'
		finally:
			print 'bye bye Pd'

def PdSocket(PORTOUT = 3005):
	if sys.platform == 'linux2':
		PD = 'pd'
	elif sys.platform == 'darwin':
		PD = '//Applications/Pd-0.42-5.app/Contents/Resources/bin'
	elif sys.platform == 'win32':
		PD = 'pd\\bin\\pd.exe'
		
	pd = Puredata()
	pd.prepare(pd = PD, dir = os.getcwd())
	pd.start()
	
	while 1:
		try:
			pd.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			pd.socket.connect(('localhost', PORTOUT))
			break
		except socket.error, (value, message):
			if pd.socket:
				pd.socket.close()
	
	pd.socket.send('python->pd Hello Pd!;\n')
	pd.socket.send('some more...;\n...messages at once;\n')

if __name__ == '__main__':
	PdSocket()


"""
PORTIN = 3006
class Listener(threading.Thread):
	def run(self):
		r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		r.bind(('localhost', PORTIN))
		r.listen(2)
		pd.send('pd pd-py-socket;')
		client_socket, address = r.accept()
		# print 'python: got a connection from ', address
		while 1:
			data = client_socket.recv(1024)
			if data:
				print "python:" , data
		r.close()

Listener().start()
"""
