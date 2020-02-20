Introduction
============

Git
---

https://github.com/ckiplab/ckipnlp

|GitHub Version| |GitHub Release| |GitHub Issues|

.. |GitHub Version| image:: https://img.shields.io/github/v/release/ckiplab/ckipnlp.svg?maxAge=3600
   :target: https://github.com/ckiplab/ckipnlp/releases

.. |GitHub License| image:: https://img.shields.io/github/license/ckiplab/ckipnlp.svg?maxAge=3600
   :target: https://github.com/ckiplab/ckipnlp/blob/master/LICENSE

.. |GitHub Release| image:: https://img.shields.io/github/release-date/ckiplab/ckipnlp.svg?maxAge=3600

.. |GitHub Downloads| image:: https://img.shields.io/github/downloads/ckiplab/ckipnlp/total.svg?maxAge=3600
   :target: https://github.com/ckiplab/ckipnlp/releases/latest

.. |GitHub Issues| image:: https://img.shields.io/github/issues/ckiplab/ckipnlp.svg?maxAge=3600
   :target: https://github.com/ckiplab/ckipnlp/issues

.. |GitHub Forks| image:: https://img.shields.io/github/forks/ckiplab/ckipnlp.svg?style=social&label=Fork&maxAge=3600

.. |GitHub Stars| image:: https://img.shields.io/github/stars/ckiplab/ckipnlp.svg?style=social&label=Star&maxAge=3600

.. |GitHub Watchers| image:: https://img.shields.io/github/watchers/ckiplab/ckipnlp.svg?style=social&label=Watch&maxAge=3600

PyPI
----

https://pypi.org/project/ckipnlp

|PyPI Version| |PyPI License| |PyPI Downloads| |PyPI Python| |PyPI Implementation| |PyPI Status|

.. |PyPI Version| image:: https://img.shields.io/pypi/v/ckipnlp.svg?maxAge=3600
   :target: https://pypi.org/project/ckipnlp

.. |PyPI License| image:: https://img.shields.io/pypi/l/ckipnlp.svg?maxAge=3600
   :target: https://github.com/ckiplab/ckipnlp/blob/master/LICENSE

.. |PyPI Downloads| image:: https://img.shields.io/pypi/dm/ckipnlp.svg?maxAge=3600
   :target: https://pypi.org/project/ckipnlp#files

.. |PyPI Python| image:: https://img.shields.io/pypi/pyversions/ckipnlp.svg?maxAge=3600

.. |PyPI Implementation| image:: https://img.shields.io/pypi/implementation/ckipnlp.svg?maxAge=3600

.. |PyPI Format| image:: https://img.shields.io/pypi/format/ckipnlp.svg?maxAge=3600

.. |PyPI Status| image:: https://img.shields.io/pypi/status/ckipnlp.svg?maxAge=3600

Documentation
-------------

https://ckipnlp.readthedocs.io/

|ReadTheDocs Home|

.. |ReadTheDocs Home| image:: https://img.shields.io/website/https/ckipnlp.readthedocs.io.svg?maxAge=3600&up_message=online&down_message=offline
   :target: http://ckipnlp.readthedocs.io

Contributers
------------

* `Mu Yang <http://muyang.pro>`_ at `CKIP <https://ckip.iis.sinica.edu.tw>`_ (Author & Maintainer)
* `Wei-Yun Ma <https://www.iis.sinica.edu.tw/pages/ma/>`_ at `CKIP <https://ckip.iis.sinica.edu.tw>`_ (Maintainer)
* `DouglasWu <dgrey1116@gmail.com>`_

External Links
--------------

- `Online Demo <https://ckip.iis.sinica.edu.tw/service/corenlp>`_

Requirements
------------

* `Python <http://www.python.org>`_ 3.5+
* `Cython <http://cython.org>`_ 0.29+
* `TreeLib <https://treelib.readthedocs.io>`_ 1.5+

.. attention::
   For Python 2 users, please use `PyCkip 0.4.2 <https://pypi.org/project/pyckip/0.4.2/>`_ instead.

CKIPWS (Optional)
^^^^^^^^^^^^^^^^^

* `CKIP Word Segmentation <http://ckip.iis.sinica.edu.tw/project/wordsegment/>`_ Linux version 20190524+

CKIPParser (Optional)
^^^^^^^^^^^^^^^^^^^^^

* `CKIP Parser <http://ckip.iis.sinica.edu.tw/project/parser/>`_ Linux version 20190506+ (20190725+ recommended)

Installation
============

Denote ``<ckipws-linux-root>`` as the root path of CKIPWS Linux Version, and ``<ckipparser-linux-root>`` as the root path of CKIPParser Linux Version.

Install Using Pip
-----------------

.. code-block:: bash

   pip install --upgrade ckipnlp
   pip install --no-deps --force-reinstall --upgrade ckipnlp \
      --install-option='--ws' \
      --install-option='--ws-dir=<ckipws-linux-root>' \
      --install-option='--parser' \
      --install-option='--parser-dir=<ckipparser-linux-root>'

Ignore ws/parser options if one doesn't have CKIPWS/CKIPParser.

Installation Options
--------------------

+-----------------------------------------------+---------------------------------------+-------------------------------+
| Option                                        | Detail                                | Default Value                 |
+===============================================+=======================================+===============================+
| ``--[no-]ws``                                 | Enable/disable CKIPWS.                | False                         |
+-----------------------------------------------+---------------------------------------+-------------------------------+
| ``--[no-]parser``                             | Enable/disable CKIPParser.            | False                         |
+-----------------------------------------------+---------------------------------------+-------------------------------+
| ``--ws-dir=<ws-dir>``                         | CKIPWS root directory.                |                               |
+-----------------------------------------------+---------------------------------------+-------------------------------+
| ``--ws-lib-dir=<ws-lib-dir>``                 | CKIPWS libraries directory            | ``<ws-dir>/lib``              |
+-----------------------------------------------+---------------------------------------+-------------------------------+
| ``--ws-share-dir=<ws-share-dir>``             | CKIPWS share directory                | ``<ws-dir>``                  |
+-----------------------------------------------+---------------------------------------+-------------------------------+
| ``--parser-dir=<parser-dir>``                 | CKIPParser root directory.            |                               |
+-----------------------------------------------+---------------------------------------+-------------------------------+
| ``--parser-lib-dir=<parser-lib-dir>``         | CKIPParser libraries directory        | ``<parser-dir>/lib``          |
+-----------------------------------------------+---------------------------------------+-------------------------------+
| ``--parser-share-dir=<parser-share-dir>``     | CKIPParser share directory            | ``<parser-dir>``              |
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


CKIPParser
-----------

.. code-block:: python

   import ckipnlp.parser
   print(ckipnlp.__name__, ckipnlp.__version__)

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

   # Show Sentence List
   ws_sents = WsSentenceList.from_text(ws_text)
   print(repr(ws_sents))
   print(ws_sents.to_text())

   # Show Each Sentence
   for ws_sent in ws_sents: print(repr(ws_sent))
   for ws_sent in ws_sents: print(ws_sent.to_text())

   # Show CkipParser output as tree
   tree_text = '#1:1.[0] S(theme:NP(possessor:N‧的(head:Nhaa:我|Head:DE:的)|Head:Nab(DUMMY1:Nab(DUMMY1:Nab:早餐|Head:Caa:、|DUMMY2:Naa:午餐)|Head:Caa:和|DUMMY2:Nab:晚餐))|quantity:Dab:都|target:PP(Head:P30:往|DUMMY:NP(property:Ncb:天|Head:Ncda:上))|Head:VA11:飛|aspect:Di:了)#'
   tree = ParserTree.from_text(tree_text)
   tree.show()

   # Get heads of tree
   for node in tree.get_heads(): print(node)

   # Get heads of node 1
   for node in tree.get_heads(1): print(node)

   # Get heads of node 2
   for node in tree.get_heads(2): print(node)

   # Get heads of node 13
   for node in tree.get_heads(13): print(node)

   # Get relations
   for rel in tree.get_relations(): print(rel)


FAQ
===

.. danger::

   Due to C code implementation, both ``CkipWs`` and ``CkipParser`` can only be instance once.

------------

.. tip::

   **The CKIPWS throws "what():  locale::facet::_S_create_c_locale name not valid". What should I do?**

   Install locale data.

   .. code-block:: bash

      apt-get install locales-all

------------

.. tip::

   **The CKIPParser throws "ImportError: libCKIPParser.so: cannot open shared object file: No such file or directory". What should I do?**

   Add below command to ``~/.bashrc``:

   .. code-block:: bash

      export LD_LIBRARY_PATH=<ckipparser-linux-root>/lib:$LD_LIBRARY_PATH

License
=======

|CC BY-NC-SA 4.0|

Copyright (c) 2018-2020 `CKIP Lab <https://ckip.iis.sinica.edu.tw>`_ under the `CC BY-NC-SA 4.0 License <http://creativecommons.org/licenses/by-nc-sa/4.0/>`_.

.. |CC BY-NC-SA 4.0| image:: https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png
   :target: http://creativecommons.org/licenses/by-nc-sa/4.0/
