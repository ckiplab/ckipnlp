Official CKIP CoreNLP Toolkits
------------------------------

Features
^^^^^^^^

- Sentence Segmentation
- Word Segmentation
- Part-of-Speech Tagging
- Named-Entity Recognition
- Sentence Parsing
- Co-Reference Resolution

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
^^^^^^^^^^^^^^

https://ckip.iis.sinica.edu.tw/service/corenlp

Contributers
^^^^^^^^^^^^

* `Mu Yang <https://muyang.pro>`_ at `CKIP <https://ckip.iis.sinica.edu.tw>`_ (Author & Maintainer)
* `Wei-Yun Ma <https://www.iis.sinica.edu.tw/pages/ma/>`_ at `CKIP <https://ckip.iis.sinica.edu.tw>`_ (Maintainer)
* `DouglasWu <dgrey1116@gmail.com>`_

Installation
------------

Requirements
^^^^^^^^^^^^

* `Python <https://www.python.org>`_ 3.6+
* `TreeLib <https://treelib.readthedocs.io>`_ 1.5+
* `CkipTagger <https://pypi.org/project/ckiptagger>`_ 0.1.1+ [Optional, Recommended]
* `CkipClassic <https://ckip-classic.readthedocs.io>`_ 1.0+ [Optional]
* `TensorFlow / TensorFlow-GPU <https://www.tensorflow.org/>`_ 1.13.1+, <2 [Required by CkipTagger]

Driver Requirements
^^^^^^^^^^^^^^^^^^^

================================  ========  ==========  ===========
Driver                            Built-in  CkipTagger  CkipClassic
================================  ========  ==========  ===========
Sentence Segmentation             ✔
Word Segmentation†                          ✔           ✔
Part-of-Speech Tagging†                     ✔           ✔
Sentence Parsing                                        ✔
Named-Entity Recognition                    ✔
Co-Reference Resolution‡          ✔         ✔           ✔
================================  ========  ==========  ===========

- † These drivers require only one of either backends.
- ‡ Co-Reference implementation does not require any backend, but requires results from word segmentation, part-of-speech tagging, sentence parsing, and named-entity recognition.

Installation via Pip
^^^^^^^^^^^^^^^^^^^^

- No backend (not recommended): ``pip install ckipnlp``.
- With CkipTagger backend (recommended): ``pip install ckipnlp[tagger]`` or ``pip install ckipnlp[tagger-gpu]``.
- With CkipClassic backend: Please refer https://ckip-classic.readthedocs.io/en/latest/main/readme.html#installation for CkipClassic installation guide.

Usage
-----

- See https://ckipnlp.readthedocs.io/en/latest/main/usage.html for Usage.
- See https://ckipnlp.readthedocs.io/en/latest/_api/ckipnlp.html for API details.

License
-------

|CC BY-NC-SA 4.0|

Copyright (c) 2018-2020 `CKIP Lab <https://ckip.iis.sinica.edu.tw>`_ under the `CC BY-NC-SA 4.0 License <http://creativecommons.org/licenses/by-nc-sa/4.0/>`_.

.. |CC BY-NC-SA 4.0| image:: https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png
   :target: http://creativecommons.org/licenses/by-nc-sa/4.0/
