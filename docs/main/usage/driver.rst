Drivers
-------

.. include:: ../_defn.rst

.. class:: Driver(*, lazy=False)
   :noindex:

   The prototype of CkipNLP Drivers.

   :param bool lazy: Lazy initialize the driver. (Call :meth:`init()` at the first call of :meth:`__call__()` instead.)

   .. method:: init()

      Initialize the driver (by calling the :meth:`_init()` function).

   .. method:: __call__(*, ...)

      Call the driver (by calling the :meth:`_call()` function).

Here are the list of the drivers:

================================  ================================  ================================  ================================
|DriverType|                      |DriverBUILTIN|                   |DriverTAGGER|                    |DriverCLASSIC|
================================  ================================  ================================  ================================
SENTENCE_SEGMENTER                |CkipSentenceSegmenter|
WORD_SEGMENTER                                                      |CkipTaggerWordSegmenter|         |CkipClassicWordSegmenter|†
POS_TAGGER                                                          |CkipTaggerPosTagger|             |CkipClassicWordSegmenter|†
NER_CHUNKER                                                         |CkipTaggerNerChunker|
CONSTITUNCY_PARSER                                                                                       |CkipClassicConstituencyParser|
COREF_CHUNKER                     |CkipCorefChunker|
================================  ================================  ================================  ================================

† Not compatible with |CkipCorefPipeline|.
