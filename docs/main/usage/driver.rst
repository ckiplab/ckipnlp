Drivers
-------

.. include:: ../_defn.rst

.. class:: Driver(*, lazy=False, ...)
   :noindex:

   The prototype of CkipNLP Drivers.

   :param bool lazy: Lazy initialize the driver. (Call :meth:`init()` at the first call of :meth:`__call__()` instead.)

   .. attribute:: driver_type
      :type: str

      The type of this driver.

   .. attribute:: driver_family
      :type: str

      The family of this driver.

   .. attribute:: driver_inputs
      :type: Tuple[str, ...]

      The inputs of this driver.

   .. method:: init()

      Initialize the driver (by calling the :meth:`_init()` function).

   .. method:: __call__(*, ...)

      Call the driver (by calling the :meth:`_call()` function).

Here are the list of the drivers:

================================  ================================  ================================  ================================  ================================
Driver Type \\ Family             ``'default'``                     ``'tagger'``                      ``'classic'``                     ``'classic-client'``
================================  ================================  ================================  ================================  ================================
Sentence Segmenter                |CkipSentenceSegmenter|
Word Segmenter                                                      |CkipTaggerWordSegmenter|         |CkipClassicWordSegmenter|†
Pos Tagger                                                          |CkipTaggerPosTagger|             |CkipClassicWordSegmenter|†
Ner Chunker                                                         |CkipTaggerNerChunker|
Constituency Parser                                                                                   |CkipClassicConParser|            |CkipClassicConParserClient|‡
Coref Chunker                     |CkipCorefChunker|
================================  ================================  ================================  ================================  ================================

- † Not compatible with |CkipCorefPipeline|.
- ‡ Please register an account at http://parser.iis.sinica.edu.tw/v1/reg.php and set the environment variables ``$CKIPPARSER_USERNAME`` and ``$CKIPPARSER_PASSWORD``.
