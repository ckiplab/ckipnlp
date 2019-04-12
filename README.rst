PyCkip
======

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
* `CKIP Word Segmentation <http://ckip.iis.sinica.edu.tw:8080/project/wordsegment/>`_ Linux version
* `CKIP Parser <http://ckip.iis.sinica.edu.tw:8080/project/parser/>`_ Linux version

Installation
------------

Denote ``<ckipws-linux-root>`` as the root path of CKIPWS Linux Version, and ``<ckipparser-linux-root>`` as the root path of CKIP-Parser Linux Version.

Step 1: Setup CKIPWS & CKIP-Parser environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Add below command to ``~/.bashrc``:

.. code-block:: bash

   export LD_LIBRARY_PATH=<ckipws-linux-root>/lib:<ckipparser-linux-root>/lib:$LD_LIBRARY_PATH


Step 2: Install Using Pip
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   pip install pyckip \
      --install-option='--ws-dir=<ckipws-linux-root>' \
      --install-option='--parser-dir=<ckipparser-linux-root>'

Installation Options
^^^^^^^^^^^^^^^^^^^^

+-----------------------------------------------+---------------------------------------+-------------------------------+
| Option                                        | Detail                                | Default Value                 |
+===============================================+=======================================+===============================+
| ``--[no-]ws``                                 | Enable/disable CKIPWS.                |                               |
+-----------------------------------------------+---------------------------------------+-------------------------------+
| ``--[no-]parser``                             | Enable/disable CKIP-Parser.           |                               |
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

API
---

CkipWS
^^^^^^

.. code-block:: python

   class ckipws.CkipWS(
      logger           = False,
      inifile          = None,
      data2dir         = None,
      lexfile          = None,
      new_style_format = False,
      show_category    = True,
   )

The CKIP word segmentation driver.

   logger (bool)
      enable logger.

   inifile (str)
      the path to the INI file.

   data2dir (str)
      the path to the folder "Data2/". (Use $CKIPWS_DATA2 if unset or null.)

   lexfile (str)
      the path to the user-defined lexicon file.

   new_style_format (bool)
      split sentences by newline characters ("\\n") rather than punctuations.

   show_category (bool)
      show part-of-speech tags.

--------------------------------

.. code-block:: python

   def ckipws.CkipWS.__call__(text, unicode=False)

Segment a sentence.

   text (str)
      the input sentence.

   unicode (bool)
      use Unicode for of input/output encoding; otherwise use system encoding.

   return value (str)
      the output sentence.

--------------------------------

.. code-block:: python

   def ckipws.CkipWS.apply_list(text, unicode=False)

Segment a list of sentence.

   ilist (str)
      the list of input sentences (str).

   unicode (bool)
      use Unicode for of input/output encoding; otherwise use system encoding.

   return value (str)
      the list of output sentences (str).

--------------------------------

.. code-block:: python

   def ckipws.CkipWS.apply_file(ifile, ofile, uwfile)

Segment a file.

   ifile (str)
      the input file.

   ofile (str)
      the output file (will be overwritten).

   uwfile (str)
      the unknown word file (will be overwritten).

CkipParser
^^^^^^^^^^

.. code-block:: python

   class ckipparser.CkipParser(
      logger           = False,
      inifile          = None,
      wsinifile        = None,
      data2dir         = None,
      ruledir          = None,
      rdbdir           = None,
      do_ws            = True,
      do_parse         = True,
      do_role          = True,
      lexfile          = None,
      new_style_format = False,
      show_category    = True,
   )

The CKIP parser driver.

   logger (bool)
      enable logger (logger is not support in parser).

   inifile (str)
      the path to the INI file.

   wsinifile (str)
      the path to the INI file.

   data2dir (str)
      the path to the folder "Data2/". (Use $CKIPWS_DATA2 if unset or null.)

   ruledir (str)
      the path to the folder "Rule/". (Use $CKIPPARSER_RULE if unset or null.)

   rdbdir (str)
      the path to the folder "RDB/". (Use $CKIPPARSER_RDB if unset or null.)

   do_ws (bool)
      do word-segmentation.

   do_parse (bool)
      do parsing.

   do_role (bool)
      do role.

   lexfile (str)
      the path to the user-defined lexicon file.

   new_style_format (bool)
      split sentences by newline characters ("\\n") rather than punctuations.

   show_category (bool)
      show part-of-speech tags.

--------------------------------

.. code-block:: python

   def ckipparser.CkipParser.__call__(text, unicode=False)

Segment a sentence.

   text (str)
      the input sentence.

   unicode (bool)
      use Unicode for of input/output encoding; otherwise use system encoding.

   return value (str)
      the output sentence.

--------------------------------

.. code-block:: python

   def ckipparser.CkipParser.apply_list(text, unicode=False)

Segment a list of sentence.

   ilist (str)
      the list of input sentences (str).

   unicode (bool)
      use Unicode for of input/output encoding; otherwise use system encoding.

   return value (str)
      the list of output sentences (str).

--------------------------------

.. code-block:: python

   def ckipparser.CkipParser.apply_file(ifile, ofile)

Segment a file.

   ifile (str)
      the input file.

   ofile (str)
      the output file (will be overwritten).

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
