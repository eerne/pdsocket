#import PdSocket, Puredata
from PdSocket import PdSocket
from Puredata import Puredata
import os

r = PdSocket()
r.prepare()
r.start()

def hello(self):
	self.send('symbol Hello\ Pd!')
	self.send('some more...;\n...messages at once')
	self.send(['list items', 'work', 'as well'])
	self.send(('tuple', 'too'))
	self.send({'key': 'value', 'more': 3})

r.onReady = hello
#r.addEvent('ready', hello)

def log(self, data):
	print 'Receive: ' + data

#r.onReceive = log
r.addEvent('receive', log)

pd = Puredata()
pd.prepare(dir = os.getcwd() + '/', file = 'pysocket-help.pd')
pd.start()

