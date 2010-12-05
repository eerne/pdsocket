"""
---

name: Puredata

version: 0.4.0-wip

authors:
- Enrique Erne

license: MIT license

...
"""
from os import system, getcwd
import os, sys, threading

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
		elif sys.platform == 'linux2':
			self.pd = 'pd'
		elif sys.platform == 'darwin':
			self.pd = '//Applications/Pd-0.42-5.app/Contents/Resources/bin/pd'
		elif sys.platform == 'win32':
			self.pd = '%programfiles%\pd\bin\pd.exe'
		return self
		
	def run(self):
		try:
			os.system('%s %s %s/%s' %(self.pd, self.args, self.dir, self.file))
		except:
			print 'couldn\'t load Pd'
		finally:
			print 'Puredata quit'



def init():
	
	pd = Puredata()
	pd.prepare(dir = os.getcwd())
	pd.start()
	

if __name__ == '__main__':
	init()

