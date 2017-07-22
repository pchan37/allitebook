Allitebook
==========

.. contents::

Project Description
-------------------
Script to download books from www.allitebooks.com

Project Instructions
--------------------
The following dependencies are required:

* Python
* Pip
* Virtualenv (via pip)

In a fresh terminal, navigate to the directory you want to store the pdf files in.  Then, execute
the following commands:

.. code-block:: bash

   $ virtualenv allitebook
   $ source allitebook/bin/activate
   $ git clone https://www.github.com/pchan37/allitebook
   $ cd allitebook
   $ pip install requirements.txt
   $ python Allitebook.py

Changelog
---------

Version 0.1.2 (in progress)
^^^^^^^^^^^^^^^^^^^^^^^^^^^
* Features the usage of a blacklist to skip certain links
* Fixed bugs when saving progress

  * AssertionError causes the program to crash before it has saved current progress
  * Progress was not saved when the program finished
* Fixed bug when determining the adjusted page to start on

  * Miscalculation lead to an off-by-one error

Version 0.1.1
^^^^^^^^^^^^^
* Features the ability to save progress with a configuration file (Press Ctrl-C)
* Features logging of broken links
* Features atomic writing of pdf and txt files

Version 0.1
^^^^^^^^^^^
* Features a downloading engine that starts from the last page and work its way to the beginning

  * Download the book in pdf format
  * Scrap the book description and save it as a .txt file
  * Scrap the book category and save both files in that folder
