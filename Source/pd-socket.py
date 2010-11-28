"""
---

name: Pd-Socket

version: 0.2.0

authors:
- Enrique Erne

license: MIT license

...
"""

import asyncore, os, socket, sys, threading

class Puredata(threading.Thread):

	def prepare(self, pd = None, dir = './', file = 'pd-socket.pd', args = '-stderr -nostdpath -rt -send \"pd dsp 1;pd dsp 0;\"'):
		self.pd = pd
		self.dir = dir
		self.file = file
		# args = -stderr -nostdpath -rt -nogui -path <path> -audiobuf <n> -nostdpath -nogui -send \"pd dsp 1;pd dsp 0;\"
		# note in -nogui you can't use -send
		self.args = args
		if pd != None:
			self.pd = pd
		else:
			if sys.platform == 'linux2':
				self.pd = 'pd'
			elif sys.platform == 'darwin':
				self.pd = '//Applications/Pd-0.42-5.app/Contents/Resources/bin'
			elif sys.platform == 'win32':
				self.pd = 'pd\\bin\\pd.exe'
		return self
		
	def run(self):
		try:
			os.system('cd %s && ./pd %s %s/%s' %(self.pd, self.args, self.dir, self.file))
		except:
			print 'couldn\'t load Pd'
		finally:
			print 'bye bye Pd'


class AsyncSocket(threading.Thread):
	
	def prepare(self):
	
		class Listen(asyncore.dispatcher_with_send):

			def handle_read(self):
				data = self.recv(8192)
				#self.send(data)
				print data

		class Open(asyncore.dispatcher):

			def __init__(self, host, port):
				asyncore.dispatcher.__init__(self)
				self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
				self.set_reuse_addr()
				self.bind((host, port))
				self.listen(1)
				print 'do something'

			def handle_accept(self):
				pair = self.accept()
				if pair is None:
					pass
				else:
					sock, addr = pair
					print 'Incoming connection from %s' % repr(addr)
					Listen(sock)
		
		self.listen = Open('localhost', 8080)
		
	def run(self):
		asyncore.loop()
		
def init(PORTOUT = 3005):
	
	receive = AsyncSocket()
	receive.prepare()
	receive.start()
	
	pd = Puredata()
	pd.prepare(dir = os.getcwd())
	pd.start()
	print 'done'
	
"""
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
"""
if __name__ == '__main__':
	init()

