========================
CombinatorialAbstractMiner
========================


Searches Scopus database for all combinations of input search terms


Description
===========

Performs searches on the Scopus database by forming all combinations of the keywords provided. It uses the pybliometrics library to access Elsevier's Scopus API.
In order to use the package, you need to obtain an API Key from https://dev.elsevier.com/. API access is included in Scopus subsciptions.
The search results are saved in an Excel-File that contains the search terms used and the article's DOI, author names, title and abstract.

Installation
============

pip install from source::

    pip install git+https://github.com/CSauerbier/CombinatorialAbstractMiner.git


Usage
=====

Enter groups of keywords as arguments, with the individual keywords delimited by commas, e.g.::
    
    caminer test1,\"test 2\" test3

will search the scopus database for the search strings
    
    TITLE-ABS-KEY(test1 AND test3)
    
    TITLE-ABS-KEY(test2 AND test3)

If you want a keyword to contain white spaces, make sure to enclose it with quotation marks as seen above 