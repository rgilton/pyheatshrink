|buildstatus|_
|appveyor|_
|coverage|_

PyHeatshrink
============

Compression using the `Heatshrink algorithm
<https://github.com/atomicobject/heatshrink>`__ in Python 3.

Installation
------------

From PyPI:

.. code-block::

   $ pip install heatshrink2

Usage
-----

Files/Streams
^^^^^^^^^^^^^

The file interface attempts to imitate the behaviour of the built-in
`file` object and other file-like objects (E.g. :code:`bz2.BZ2File`),
thus you can expect all methods implemented in :code:`file` to also be
available.

You can open a heatshrink file by using the :code:`open` function:

.. code-block:: python

   >>> import heatshrink2
   >>> with heatshrink2.open('data.bin', 'wb') as fout:
   ...     fout.write(b"Is there anybody in there?")
   ...
   26
   >>>

You can also use :code:`HeatshrinkFile` directly:

.. code-block:: python

   >>> from heatshrink2 import HeatshrinkFile
   >>> with HeatshrinkFile('data.bin') as fin:
   ...     print(fin.read(256))
   ...
   b'Is there anybody in there?'
   >>> with HeatshrinkFile('data.bin') as fin:
   ...     for line in fin:
   ...         print(line)
   ...
   b'Is there anybody in there?'
   >>>

Byte strings
^^^^^^^^^^^^

The encoder accepts any iterable and returns a byte string
containing encoded (compressed) data.

.. code-block:: python

   >>> import heatshrink2
   >>> heatshrink2.compress(b'a string')
   b'\xb0\xc8.wK\x95\xa6\xddg'
   >>>

The decoder accepts any object that implements the buffer protocol and
returns a byte representation of the decoded data.

.. code-block:: python

   >>> import heatshrink2
   >>> heatshrink2.decompress(b'\xb0\xc8.wK\x95\xa6\xddg')
   b'a string'
   >>>

Parameters
^^^^^^^^^^

Both the encoder and decoder allow providing :code:`window_sz2` and
:code:`lookahead_sz2` keywords:

:code:`window_sz2` - The window size determines how far back in the
input can be searched for repeated patterns. A window_sz2 of 8 will
only use 256 bytes (2^8), while a window_sz2 of 10 will use 1024 bytes
(2^10). The latter uses more memory, but may also compress more
effectively by detecting more repetition.

:code:`lookahead_sz2` - The lookahead size determines the max length
for repeated patterns that are found. If the lookahead_sz2 is 4, a
50-byte run of 'a' characters will be represented as several repeated
16-byte patterns (2^4 is 16), whereas a larger lookahead_sz2 may be
able to represent it all at once. The number of bits used for the
lookahead size is fixed, so an overly large lookahead size can reduce
compression by adding unused size bits to small patterns.

:code:`input_buffer_size` - How large an input buffer to use for the
decoder. This impacts how much work the decoder can do in a single
step, and a larger buffer will use more memory. An extremely small
buffer (say, 1 byte) will add overhead due to lots of suspend/resume
function calls, but should not change how well data compresses.

Check out the `heatshrink configuration page
<https://github.com/atomicobject/heatshrink#configuration>`__ for more
details.

For more use cases, please refer to the `tests folder
<https://github.com/eerimoq/pyheatshrink/blob/master/tests>`__.

Command line
------------

The command line tool can compress and decompress files.

Below is an example of the compress and decompress subcommands.

.. code-block::

   $ ls -l tests/files/foo.txt
   -rw-rw-r-- 1 erik erik 3970 jan  5 12:23 tests/files/foo.txt
   $ python -m heatshrink2 compress tests/files/foo.txt foo.hs
   $ ls -l foo.hs
   -rw-rw-r-- 1 erik erik 2727 jan  5 12:24 foo.hs
   $ python -m heatshrink2 decompress foo.hs foo.txt
   $ cmp tests/files/foo.txt foo.txt

Benchmarks
----------

The benchmarks check compression/decompression against a ~6MB file:

.. code-block::

   $ python scripts/benchmark.py

Testing
-------

Running tests is as simple as doing:

.. code-block::

    $ python setup.py test

License
-------

ISC license

.. |buildstatus| image:: https://travis-ci.com/eerimoq/pyheatshrink.svg?branch=master
.. _buildstatus: https://travis-ci.com/eerimoq/pyheatshrink

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/eerimoq/pyheatshrink?svg=true
.. _appveyor: https://ci.appveyor.com/project/eerimoq/pyheatshrink/branch/master

.. |coverage| image:: https://coveralls.io/repos/github/eerimoq/pyheatshrink/badge.svg?branch=master
.. _coverage: https://coveralls.io/github/eerimoq/pyheatshrink
