Usage
=====

.. include:: _defn.rst

CkipNLP provides a set of human language technology tools, including

- Sentence Segmentation
- Word Segmentation
- Part-of-Speech Tagging
- Named-Entity Recognition
- Constituency Parsing
- Coreference Resolution

The library is build around three types of classes:

- `Containers <usage/container.html>`_ such as |SegParagraph| are the basic data structures for inputs and outputs.

- `Drivers <usage/driver.html>`_ such as |CkipTaggerWordSegmenter| that apply specific tool on the inputs.

- `Pipelines <usage/pipeline.html>`_ such as |CkipPipeline| are collections of drivers that automatically handles the dependencies between inputs and outputs.

.. toctree::
   :hidden:

   usage/container
   usage/driver
   usage/pipeline
