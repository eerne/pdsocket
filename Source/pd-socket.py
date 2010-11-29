"""
---

name: Pd-Socket

version: 0.2.0-wip

authors:
- Enrique Erne

license: MIT license

...
"""

import asyncore, os, socket, sys, threading, time

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
				self.pd = '//Applications/Pd-0.42-5.app/Contents/Resources/bin/pd'
			elif sys.platform == 'win32':
				#self.pd = 'pd\\bin\\pd.exe'
				self.pd = '%programfiles%\pd\bin\pd.exe'
		return self
		
	def run(self):
		try:
			os.system('%s %s %s/%s' %(self.pd, self.args, self.dir, self.file))
		except:
			print 'couldn\'t load Pd'
		finally:
			print 'bye bye Pd'


class AsyncSocket(threading.Thread):
	
	def prepare(self):
	
		class Listen(asyncore.dispatcher_with_send):

			def handle_read(that):
				data = that.recv(8192)
				#self.send(data)
				print data

			def handle_close(that):
				that.close()
				exit()
		
		class Connect():
			
			def __init__(that):
				try:
					self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					self.socket.connect(('localhost', 3005))
				except socket.error, (value, message):
					if self.socket:
						self.socket.close()
		
		
		class Open(asyncore.dispatcher):

			def __init__(that, host, port):
				asyncore.dispatcher.__init__(that)
				that.create_socket(socket.AF_INET, socket.SOCK_STREAM)
				that.set_reuse_addr()
				that.bind((host, port))
				that.listen(1)
				print 'do something'

			def handle_accept(that):
				pair = that.accept()
				if pair is None:
					pass
				else:
					sock, addr = pair
					print 'Incoming connection from %s' % repr(addr)
					Connect()
					Listen(sock)
		
		Open('localhost', 8080)
		
	def run(self):
		self.loop = asyncore.loop()
	
	def send(self, data = ''):
		self.socket.send(data + ';\n')
		
def init():
	
	r = AsyncSocket()
	r.prepare()
	r.start()
	
	pd = Puredata()
	pd.prepare(dir = os.getcwd())
	pd.start()
	print 'done'
	
	time.sleep(6)
	r.send('python->pd Hello Pd!')
	r.send('some more...;\n...messages at once')
	

if __name__ == '__main__':
	init()

