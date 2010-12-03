Pd-Socket
=========

Python class for opening Puredata and connecting on a socket with [netreceive].

Read more about Puredata aka Pd on [crca.ucsd.edu/~msp/software.html](http://crca.ucsd.edu/~msp/software.html)

How to use
----------
	
	cd Pd-Socket/Source/
	python pd-socket.py

### Messages

The networking protocol sent to Pd is [FUDI](http://en.wikipedia.org/wiki/FUDI) and messages need to end with `;\n`

	pd.send('Hello Pd!;\n')
	pd.send('some more...;\n...messages at once;\n')


### Todo

 * test on win
 * close method for Pd-Socket
 * Pd-0.43 compatibility
 * write test
 * build as package


Author(s)
---------

 * Enrique Erne


### Related Projects

 * [github.com/automata/topd](https://github.com/automata/topd/), [automata.cc/wiki/Main/ToPD](http://automata.cc/wiki/Main/ToPD)
 * [code.google.com/p/pyata](http://code.google.com/p/pyata/)
 * [mccormick.cx/projects/PyPd](http://mccormick.cx/projects/PyPd/)
