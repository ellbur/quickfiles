
This is a small file path manipulation DSL for Python.

Examples
--------

	from quickfiles import *

Find directory where script is located.

	here = p(__file__).dir

	tmp_dir = here / 'tmp'
	tmp_dir.mkdir()

Make a unique file name with a prefix.

	a = tmp_dir % COUNTER('hello')

Set the file's contents.

	a.set('Hello, world!')

Read the file's contents.

	print(a.read())

Two more unique file names, which are directories.

	b1 = tmp_dir % COUNTER('hello')
	b1.mkdir()

	b2 = tmp_dir % COUNTER('hello')
	b2.mkdir()

Make a file in that directory, with random name.

	c1 = b1 % RAND('c', '.txt')
	c1.set('Trapped in a file.')

Find the file with the same path relative to b2.

	c2 = c1.replant(b1, b2)

Copy the contents over.

	c1.cp(c2)

Verify that it got there.

	print(c2.read())

Clean up.

	tmp_dir.rm()

