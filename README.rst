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

Requirements
------------

* `Python <http://www.python.org>`_ 3.5+
* `Cython <http://cython.org>`_ 0.29+

CkipWs (Optional)
^^^^^^^^^^^^^^^^^

* `CKIP Word Segmentation <http://ckip.iis.sinica.edu.tw/project/wordsegment/>`_ Linux version (20190524+)

CkipParser (Optional)
^^^^^^^^^^^^^^^^^^^^^

* `CKIP Parser <http://ckip.iis.sinica.edu.tw/project/parser/>`_ Linux version (20190506+)
* `Boost C++ Libraries <https://www.boost.org/>`_ 1.54.0

Installation
============

Denote ``<ckipws-linux-root>`` as the root path of CKIPWS Linux Version, and ``<ckipparser-linux-root>`` as the root path of CKIP-Parser Linux Version.

Step 1: Setup CKIPWS & CKIP-Parser environment
----------------------------------------------

Add below command to ``~/.bashrc``:

.. code-block:: bash

   export LD_LIBRARY_PATH=<ckipws-linux-root>/lib:<ckipparser-linux-root>/lib:$LD_LIBRARY_PATH


Step 2: Install Using Pip
-------------------------

.. code-block:: bash

   pip install ckipnlp \
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

FAQ
===

* The CKIPWS throws "``what():  locale::facet::_S_create_c_locale name not valid``". What should I do?

.. code-block:: bash

   apt-get install locales-all

License
=======

* `MIT License <LICENSE>`_
