PyCkip
========

CKIP NLP Wrappers (Word Segmentation and Parser)

Introduction
------------

Git
^^^

https://github.com/emfomy/pyckip

|Github Release| |Github License| |Github Forks| |Github Stars| |Github Watchers|

.. |Github Release| image:: https://img.shields.io/github/release/emfomy/pyckip/all.svg?maxAge=3600
   :target: https://github.com/emfomy/pyckip/releases

.. |Github License| image:: https://img.shields.io/github/license/emfomy/pyckip.svg?maxAge=3600

.. |Github Downloads| image:: https://img.shields.io/github/downloads/emfomy/pyckip/total.svg?maxAge=3600
   :target: https://github.com/emfomy/pyckip/releases/latest

.. |Github Forks| image:: https://img.shields.io/github/forks/emfomy/pyckip.svg?style=social&label=Fork&maxAge=3600

.. |Github Stars| image:: https://img.shields.io/github/stars/emfomy/pyckip.svg?style=social&label=Star&maxAge=3600

.. |Github Watchers| image:: https://img.shields.io/github/watchers/emfomy/pyckip.svg?style=social&label=Watch&maxAge=3600

PyPI
^^^^

https://pypi.org/project/pyckip

|Pypi Version| |Pypi License| |Pypi Format| |Pypi Python| |Pypi Implementation| |Pypi Status|

.. |Pypi Version| image:: https://img.shields.io/pypi/v/pyckip.svg?maxAge=3600
   :target: https://pypi.org/project/pyckip

.. |Pypi License| image:: https://img.shields.io/pypi/l/pyckip.svg?maxAge=3600

.. |Pypi Format| image:: https://img.shields.io/pypi/format/pyckip.svg?maxAge=3600

.. |Pypi Python| image:: https://img.shields.io/pypi/pyversions/pyckip.svg?maxAge=3600

.. |Pypi Implementation| image:: https://img.shields.io/pypi/implementation/pyckip.svg?maxAge=3600

.. |Pypi Status| image:: https://img.shields.io/pypi/status/pyckip.svg?maxAge=3600

Author
^^^^^^

* Mu Yang <emfomy@gmail.com>

Requirements
^^^^^^^^^^^^

* `Python <http://www.python.org>`_ 2.7+, 3.5+
* `Cython <http://cython.org>`_ 0.29+
* `Boost C++ Libraries <https://www.boost.org/>`_ 1.54.0
* CKIP Word Segmentation Linux version
* CKIP Parser Linux version

Installation
^^^^^^^^^^^^

Step 1: Setup CKIPWS environment
""""""""""""""""""""""""""""""""

Denote ``<ckipws-linux-root>`` as the root path of CKIPWS Linux Version. Add below command to ``~/.bashrc``

.. code-block:: bash

   export LD_LIBRARY_PATH=<ckipws-linux-root>/lib:$LD_LIBRARY_PATH
   export CKIPWS_DATA2=<ckipws-linux-root>/Data2

Step 2: Setup CKIP-Parser environment
"""""""""""""""""""""""""""""""""""""

Denote ``<ckipparser-linux-root>`` as the root path of CKIP-Parser Linux Version. Add below command to ``~/.bashrc``

.. code-block:: bash

   export LD_LIBRARY_PATH=<ckipparser-linux-root>/lib:$LD_LIBRARY_PATH
   export CKIPPARSER_RULE=<ckipparser-linux-root>/Rule
   export CKIPPARSER_RDB=<ckipparser-linux-root>/RDB

Step 3: Install Using Pip
"""""""""""""""""""""""""

.. code-block:: bash

   LIBRARY_PATH=<ckipws-linux-root>/lib:<ckipparser-linux-root>/lib:$LIBRARY_PATH pip install pyckip

FAQ
---

* I don't have CKIPWS/CKIP-Parser. What should I do?

Append :code:`--install-option='--no-ws'` or :code:`--install-option='--no-parser'` after the :code:`pip install` command to disable CKIPWS or CKIP-Parser.

.. code-block:: bash

   # Disable CKIPWS support
   pip install pyckip --install-option='--no-ws'

   # Disable CKIP-Parser support
   pip install pyckip --install-option='--no-parser'

* The CKIPWS throws "``what():  locale::facet::_S_create_c_locale name not valid``". What should I do?

.. code-block:: bash

   apt-get install locales-all

License
-------

* `MIT License <LICENSE>`_
