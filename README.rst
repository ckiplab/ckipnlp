Introduction
============

Official CKIP CoreNLP Toolkits

Features
--------

- Sentence Segmentation
- Word Segmentation
- Part-of-Speech Tagging
- Sentence Parsing
- Named-Entity Recognition
- Co-Reference Delectation

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

Installation
============

Requirements
------------

* `Python <http://www.python.org>`_ 3.6+
* `TreeLib <https://treelib.readthedocs.io>`_ 1.5+

* `CkipTagger <https://pypi.org/project/ckiptagger>`_ 0.1.1+ [Optional, Recommended]
* `CkipClassic <https://ckip-classic.readthedocs.io>`_ 1.0+ [Optional]

Tool Requirements
-----------------

================================  ========  ==========  ===========
Tool                              Built-in  CkipTagger  CkipClassic
================================  ========  ==========  ===========
Sentence Segmentation             ✔
Word Segmentation†                          ✔           ✔
Part-of-Speech Tagging†                     ✔           ✔
Sentence Parsing                                        ✔
Named-Entity Recognition                    ✔
Co-Reference Delectation‡         ✔         ✔           ✔
================================  ========  ==========  ===========

- † These tools require only one of either backends.
- ‡ Co-Reference implementation does not require any backend, but requires results from word segmentation, part-of-speech tagging, sentence parsing, and named-entity recognition.

Installation via Pip
--------------------

- No backend (not recommended): ``pip install ckipnlp``.
- With CkipTagger backend (recommended): ``pip install ckipnlp[tagger]``.
- With CkipClassic backend: ``pip install ckipnlp[classic]``.
- With both backend: ``pip install ckipnlp[tagger,classic]``.

Please refer https://ckip-classic.readthedocs.io for CkipClassic installation guide.

Usage
=====

See https://ckipnlp.readthedocs.io/en/latest/_api/ckipnlp.html for API details.

Pipelines
---------

Core Pipeline
^^^^^^^^^^^^^

.. image:: _static/image/pipeline.svg

.. code-block:: python

   from ckipnlp.pipeline import CkipPipeline, CkipDocument

   pipeline = CkipPipeline()
   doc = CkipDocument(
      raw='中文字喔，啊哈哈哈',
   )

   # Word Segmentation
   pipeline.get_ws(doc)
   print(doc.ws)
   for line in doc.ws:
       print(line.to_text())

   # Part-of-Speech Tagging
   pipeline.get_pos(doc)
   print(doc.pos)
   for line in doc.pos:
       print(line.to_text())

   # Named-Entity Recognition
   pipeline.get_ner(doc)
   print(doc.ner)

   # Sentence Parsing
   pipeline.get_parsed(doc)
   print(doc.parsed)

   ################################################################

   from ckipnlp.container.util.wspos import WsPosParagraph

   # Word Segmentation & Part-of-Speech Tagging
   for line in WsPosParagraph.to_text(doc.ws, doc.pos):
       print(line)

Co-Reference Pipeline
^^^^^^^^^^^^^^^^^^^^^

.. image:: _static/image/coref_pipeline.svg

.. code-block:: python

   from ckipnlp.pipeline import CkipCorefPipeline, CkipDocument

   pipeline = CkipCorefPipeline()
   doc = CkipDocument(
      raw='畢卡索他想，完蛋了',
   )

   # Co-Reference
   corefdoc = pipeline(doc)
   print(corefdoc.coref)
   for line in corefdoc.coref:
       print(line.to_text())

Containers
----------

The container objects provides following methods:

-  |from_text|, |to_text| for plain-text format conversions;
-  |from_dict|, |to_dict| for dictionary-like format conversions;
-  |from_list|, |to_list| for list-like format conversions;
-  |from_json|, |to_json| for JSON format conversions (based-on dictionary-like format conversions).

The following are the interfaces, where ``CONTAINER_CLASS`` refers to the container class.

.. code-block:: python

   obj = CONTAINER_CLASS.from_text(plain_text)
   plain_text = obj.to_text()

   obj = CONTAINER_CLASS.from_dict({ key: value })
   dict_obj = obj.to_dict()

   obj = CONTAINER_CLASS.from_list([ value1, value2 ])
   list_obj = obj.to_list()

   obj = CONTAINER_CLASS.from_json(json_str)
   json_str = obj.to_json()

Note that not all container provide all above methods. Here is the table of implemented methods. Please refer the documentation of each container for detail formats.

========================  ========================  ============  ========================
Container                 Item                      from/to text  from/to dict, list, json
========================  ========================  ============  ========================
|TextParagraph|           |str|                     ✔             ✔
|SegSentence|             |str|                     ✔             ✔
|SegParagraph|            |SegSentence|             ✔             ✔
|NerToken|                ✘                                       ✔
|NerSentence|             |NerToken|                              ✔
|NerParagraph|            |NerSentence|                           ✔
|ParsedParagraph|         |str|                     ✔             ✔
|CorefToken|              ✘                         only to       ✔
|CorefSentence|           |CorefToken|              only to       ✔
|CorefParagraph|          |CorefSentence|           only to       ✔
========================  ========================  ============  ========================

WS with POS
^^^^^^^^^^^

There are also conversion routines for word-segmentation and POS containers jointly. For example, |WsPosToken| provides routines for a word (|str|) with POS-tag (|str|):

.. code-block:: python

   ws_obj, pos_obj = WsPosToken.from_text('中文字(Na)')
   plain_text = WsPosToken.to_text(ws_obj, pos_obj)

   ws_obj, pos_obj = WsPosToken.from_dict({ 'word': '中文字', 'pos': 'Na', })
   dict_obj = WsPosToken.to_dict(ws_obj, pos_obj)

   ws_obj, pos_obj = WsPosToken.from_list([ '中文字', 'Na' ])
   list_obj = WsPosToken.to_list(ws_obj, pos_obj)

   ws_obj, pos_obj = WsPosToken.from_json(json_str)
   json_str = WsPosToken.to_json(ws_obj, pos_obj)

Similarly, |WsPosSentence|/|WsPosParagraph| provides routines for word-segmented and POS sentence/paragraph (|SegSentence|/|SegParagraph|) respectively.

Parsed Tree
^^^^^^^^^^^

License
=======

|CC BY-NC-SA 4.0|

Copyright (c) 2018-2020 `CKIP Lab <https://ckip.iis.sinica.edu.tw>`_ under the `CC BY-NC-SA 4.0 License <http://creativecommons.org/licenses/by-nc-sa/4.0/>`_.

.. |CC BY-NC-SA 4.0| image:: https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png
   :target: http://creativecommons.org/licenses/by-nc-sa/4.0/



.. |from_text| replace:: ``from_text()``
.. |to_text| replace:: ``to_text()``
.. |from_dict| replace:: ``from_dict()``
.. |to_dict| replace:: ``to_dict()``
.. |from_list| replace:: ``from_list()``
.. |to_list| replace:: ``to_list()``
.. |from_json| replace:: ``from_json()``
.. |to_json| replace:: ``to_json()``

.. |str| replace:: ``str``

.. |TextParagraph| replace:: ``TextParagraph``
.. |SegSentence| replace:: ``SegSentence``
.. |SegParagraph| replace:: ``SegParagraph``
.. |NerToken| replace:: ``NerToken``
.. |NerSentence| replace:: ``NerSentence``
.. |NerParagraph| replace:: ``NerParagraph``
.. |ParsedParagraph| replace:: ``ParsedParagraph``
.. |CorefToken| replace:: ``CorefToken``
.. |CorefSentence| replace:: ``CorefSentence``
.. |CorefParagraph| replace:: ``CorefParagraph``

.. |WsPosToken| replace:: ``WsPosToken``
.. |WsPosSentence| replace:: ``WsPosSentence``
.. |WsPosParagraph| replace:: ``WsPosParagraph``

.. |ParsedNodeData| replace:: ``ParsedNodeData``
.. |ParsedNode| replace:: ``ParsedNode``
.. |ParsedRelation| replace:: ``ParsedRelation``
.. |ParsedTree| replace:: ``ParsedTree``
