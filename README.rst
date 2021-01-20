CKIP CoreNLP Toolkit
--------------------

Features
^^^^^^^^

- Sentence Segmentation
- Word Segmentation
- Part-of-Speech Tagging
- Named-Entity Recognition
- Constituency Parsing
- Coreference Resolution

Git
^^^

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
^^^^

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
^^^^^^^^^^^^^

https://ckipnlp.readthedocs.io/

|ReadTheDocs Home|

.. |ReadTheDocs Home| image:: https://img.shields.io/website/https/ckipnlp.readthedocs.io.svg?maxAge=3600&up_message=online&down_message=offline
   :target: https://ckipnlp.readthedocs.io

Online Demo
^^^^^^^^^^^

https://ckip.iis.sinica.edu.tw/service/corenlp

Contributers
^^^^^^^^^^^^

* `Mu Yang <https://muyang.pro>`__ at `CKIP <https://ckip.iis.sinica.edu.tw>`__ (Author & Maintainer)
* `Wei-Yun Ma <https://www.iis.sinica.edu.tw/pages/ma/>`__ at `CKIP <https://ckip.iis.sinica.edu.tw>`__ (Maintainer)
* `DouglasWu <dgrey1116@gmail.com>`__

Installation
------------

Requirements
^^^^^^^^^^^^

* `Python <https://www.python.org>`__ 3.6+
* `TreeLib <https://treelib.readthedocs.io>`__ 1.5+
* `CkipTagger <https://pypi.org/project/ckiptagger>`__ 0.2.1+ [Optional, Recommended]
* `CkipClassic <https://ckip-classic.readthedocs.io>`__ 1.0+ [Optional, Recommended]
* `TensorFlow / TensorFlow-GPU <https://www.tensorflow.org/>`__ 1.13.1+ [Required by CkipTagger]

Driver Requirements
^^^^^^^^^^^^^^^^^^^

================================  ========  ==========  ===========
Driver                            Built-in  CkipTagger  CkipClassic
================================  ========  ==========  ===========
Sentence Segmentation             ✔
Word Segmentation†                          ✔           ✔
Part-of-Speech Tagging†                     ✔           ✔
Constituency Parsing                                    ✔
Named-Entity Recognition                    ✔
Coreference Resolution‡           ✔         ✔           ✔
================================  ========  ==========  ===========

- † These drivers require only one of either backends.
- ‡ Coreference implementation does not require any backend, but requires results from word segmentation, part-of-speech tagging, constituency parsing, and named-entity recognition.

Installation via Pip
^^^^^^^^^^^^^^^^^^^^

- No backend (not recommended): ``pip install ckipnlp``.
- With CkipTagger backend (recommended): ``pip install ckipnlp[tagger]`` or ``pip install ckipnlp[tagger-gpu]``.
- With CkipClassic Parser Client backend (recommended): ``pip install ckipnlp[classic]``.
- With CkipClassic offline backend: Please refer https://ckip-classic.readthedocs.io/en/latest/main/readme.html#installation for CkipClassic installation guide.

.. attention::
   To use CkipClassic Parser Client backend, please

   #. Register an account at http://parser.iis.sinica.edu.tw/v1/reg.exe
   #. Set the environment variables ``$CKIPPARSER_USERNAME`` and ``$CKIPPARSER_PASSWORD`` to the username and password.

Detail
------

See https://ckipnlp.readthedocs.io/ for full documentation.

License
-------

|GPL-3.0|

Copyright (c) 2018-2020 `CKIP Lab <https://ckip.iis.sinica.edu.tw>`__ under the `GPL-3.0 License <https://www.gnu.org/licenses/gpl-3.0.html>`__.

.. |GPL-3.0| image:: https://www.gnu.org/graphics/gplv3-with-text-136x68.png
   :target: https://www.gnu.org/licenses/gpl-3.0.html
