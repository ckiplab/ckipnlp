Introduction
============

Git
---

https://github.com/emfomy/ckipnlp

|Github Release| |Github License| |Github Forks| |Github Stars| |Github Watchers|

.. |Github Release| image:: https://img.shields.io/github/release/emfomy/ckipnlp/all.svg?maxAge=3600
   :target: https://github.com/emfomy/ckipnlp/releases

.. |Github License| image:: https://img.shields.io/github/license/emfomy/ckipnlp.svg?maxAge=3600

.. |Github Downloads| image:: https://img.shields.io/github/downloads/emfomy/ckipnlp/total.svg?maxAge=3600
   :target: https://github.com/emfomy/ckipnlp/releases/latest

.. |Github Forks| image:: https://img.shields.io/github/forks/emfomy/ckipnlp.svg?style=social&label=Fork&maxAge=3600

.. |Github Stars| image:: https://img.shields.io/github/stars/emfomy/ckipnlp.svg?style=social&label=Star&maxAge=3600

.. |Github Watchers| image:: https://img.shields.io/github/watchers/emfomy/ckipnlp.svg?style=social&label=Watch&maxAge=3600

PyPI
----

https://pypi.org/project/ckipnlp

|Pypi Version| |Pypi License| |Pypi Format| |Pypi Python| |Pypi Implementation| |Pypi Status|

.. |Pypi Version| image:: https://img.shields.io/pypi/v/ckipnlp.svg?maxAge=3600
   :target: https://pypi.org/project/ckipnlp

.. |Pypi License| image:: https://img.shields.io/pypi/l/ckipnlp.svg?maxAge=3600

.. |Pypi Format| image:: https://img.shields.io/pypi/format/ckipnlp.svg?maxAge=3600

.. |Pypi Python| image:: https://img.shields.io/pypi/pyversions/ckipnlp.svg?maxAge=3600

.. |Pypi Implementation| image:: https://img.shields.io/pypi/implementation/ckipnlp.svg?maxAge=3600

.. |Pypi Status| image:: https://img.shields.io/pypi/status/ckipnlp.svg?maxAge=3600

Author
------

* Mu Yang <emfomy@gmail.com>

Documentation
-------------

http://ckipnlp.readthedocs.io/

Requirements
------------

* `Python <http://www.python.org>`_ 3.5+
* `Cython <http://cython.org>`_ 0.29+

.. note::
   For Python 2 users, please use `PyCkip 0.4.2 <https://pypi.org/project/pyckip/0.4.2/>`_ instead.

CkipWs (Optional)
^^^^^^^^^^^^^^^^^

* `CKIP Word Segmentation <http://ckip.iis.sinica.edu.tw/project/wordsegment/>`_ Linux version 20190524+

CkipParser (Optional)
^^^^^^^^^^^^^^^^^^^^^

* `CKIP Parser <http://ckip.iis.sinica.edu.tw/project/parser/>`_ Linux version 20190506+ (20190725+ recommended)

Installation
============

Denote ``<ckipws-linux-root>`` as the root path of CKIPWS Linux Version, and ``<ckipparser-linux-root>`` as the root path of CKIP-Parser Linux Version.

Install Using Pip
-----------------

.. code-block:: bash

   pip install --upgrade ckipnlp
   pip install --no-deps --force-reinstall --upgrade ckipnlp \
      --install-option='--ws' \
      --install-option='--ws-dir=<ckipws-linux-root>' \
      --install-option='--parser' \
      --install-option='--parser-dir=<ckipparser-linux-root>'

Ignore ws/parser options if one doesn't have CKIPWS/CKIP-Parser.

Installation Options
--------------------

+-----------------------------------------------+---------------------------------------+-------------------------------+
| Option                                        | Detail                                | Default Value                 |
+===============================================+=======================================+===============================+
| ``--[no-]ws``                                 | Enable/disable CKIPWS.                | False                         |
+-----------------------------------------------+---------------------------------------+-------------------------------+
| ``--[no-]parser``                             | Enable/disable CKIP-Parser.           | False                         |
+-----------------------------------------------+---------------------------------------+-------------------------------+
| ``--ws-dir=<ws-dir>``                         | CKIPWS root directory.                |                               |
+-----------------------------------------------+---------------------------------------+-------------------------------+
| ``--ws-lib-dir=<ws-lib-dir>``                 | CKIPWS libraries directory            | ``<ws-dir>/lib``              |
+-----------------------------------------------+---------------------------------------+-------------------------------+
| ``--ws-share-dir=<ws-share-dir>``             | CKIPWS share directory                | ``<ws-dir>``                  |
+-----------------------------------------------+---------------------------------------+-------------------------------+
| ``--parser-dir=<parser-dir>``                 | CKIP-Parser root directory.           |                               |
+-----------------------------------------------+---------------------------------------+-------------------------------+
| ``--parser-lib-dir=<parser-lib-dir>``         | CKIP-Parser libraries directory       | ``<parser-dir>/lib``          |
+-----------------------------------------------+---------------------------------------+-------------------------------+
| ``--parser-share-dir=<parser-share-dir>``     | CKIP-Parser share directory           | ``<parser-dir>``              |
+-----------------------------------------------+---------------------------------------+-------------------------------+
| ``--data2-dir=<data2-dir>``                   | "Data2" directory                     | ``<ws-share-dir>/Data2``      |
+-----------------------------------------------+---------------------------------------+-------------------------------+
| ``--rule-dir=<rule-dir>``                     | "Rule" directory                      | ``<parser-share-dir>/Rule``   |
+-----------------------------------------------+---------------------------------------+-------------------------------+
| ``--rdb-dir=<rdb-dir>``                       | "RDB" directory                       | ``<parser-share-dir>/RDB``    |
+-----------------------------------------------+---------------------------------------+-------------------------------+

Usage
=====

See http://ckipnlp.readthedocs.io/ for API details.

CKIPWS
------

.. code-block:: python

   import ckipnlp.ws
   print(ckipnlp.__name__, ckipnlp.__version__)

   ws = ckipnlp.ws.CkipWs(logger=False)
   print(ws('中文字喔'))
   for l in ws.apply_list(['中文字喔', '啊哈哈哈']): print(l)

   ws.apply_file(ifile='sample/sample.txt', ofile='output/sample.tag', uwfile='output/sample.uw')
   with open('output/sample.tag') as fin:
       print(fin.read())
   with open('output/sample.uw') as fin:
       print(fin.read())


CKIP-Parser
-----------

.. code-block:: python

   import ckipnlp.parser
   print(ckipnlp.__name__, ckipnlp.__version__)

   ps = ckipnlp.parser.CkipParser(logger=False)
   print(ps('中文字喔'))
   for l in ps.apply_list(['中文字喔', '啊哈哈哈']): print(l)

   ps = ckipnlp.parser.CkipParser(logger=False)
   print(ps('中文字喔'))
   for l in ps.apply_list(['中文字喔', '啊哈哈哈']): print(l)
   ps.apply_file(ifile='sample/sample.txt', ofile='output/sample.tree')
   with open('output/sample.tree') as fin:
       print(fin.read())

Utilities
---------

.. code-block:: python

   import ckipnlp
   print(ckipnlp.__name__, ckipnlp.__version__)

   from ckipnlp.util.ws import *
   from ckipnlp.util.parser import *

   # Format CkipWs output
   ws_text = ['中文字(Na)　喔(T)', '啊哈(I)　哈哈(D)']
   for text in ws_text: print(ckipnlp.util.ws.WsSentence.from_text(text))
   for text in ws_text: print(repr(ckipnlp.util.ws.WsSentence.from_text(text)))

   # Show CkipParser output as tree
   tree_text = 'S(theme:NP(property:N‧的(head:Nhaa:我|Head:DE:的)|Head:Nad(DUMMY1:Nab:早餐|Head:Caa:和|DUMMY2:Naa:午餐))|quantity:Dab:都|Head:VC31:吃完|aspect:Di:了)'
   tree = ParserTree.from_text(tree_text)
   tree.show()

   # Get dummies of node 5
   for node in tree.get_dummies(5): print(node)

   # Get heads of node 1
   for node in tree.get_heads(1): print(node)

   # Get relations
   for r in tree.get_relations(0): print(r)


FAQ
===

.. warning::

   The CKIPWS throws "``what():  locale::facet::_S_create_c_locale name not valid``". What should I do?

Install locale data.

.. code-block:: bash

   apt-get install locales-all

.. warning::

   The CKIPParser throws "``ImportError: libCKIPParser.so: cannot open shared object file: No such file or directory``". What should I do?

Add below command to ``~/.bashrc``:

.. code-block:: bash

   export LD_LIBRARY_PATH=<ckipparser-linux-root>/lib:$LD_LIBRARY_PATH

License
=======

* `MIT License <LICENSE>`_
