# Terminology Extraction
This is a project where we use Yake and word embeddings to extract key terminology from a set of 2024 Election news sources.

## Document Extractor
This folder consists of a basic webscraper that uses user inputs to create documents with the text of different news sources. We are using this to develop our training, development, and test corpuses. The two files on this are clickLink.py, which extracts the text from each link that is parsed through using a selenium scraper. The newsAPIscraper.py file uses a news API to collect a set of sources using a query and a number of documents. It then develops the files for the corpuses used. 

## Corpuses
This folder consists of txt files with our training, dev, and test corpuses
