# Terminology Extraction

## Project Description
This is a project where we use Yake and word embeddings to extract key terminology from a set of 2024 Election news sources.

### Process
For this project, we used a newsAPI to collect a set of links from the internet of news sources that related to the 2024 US Election. We found these by using the keyword 'US 2024 Election.' From there, we used selenium to build a webscraper that pulled the HTML from different news sources. We used this to create our development and training data. We then found existing news sources on the internet using the 'US 2024 Election' keywords and created a ground truth based on three sets of manual annotations. We used the existing selenium scraper, which was used to collect the plain text article content from each link from the NewsAPI, and ran this scraper on the links that we collected. This made up our test data.

Using our training data, we used existing ginsem word2vec libraries to generate vectors for each keyword in the training data. Then, we split up each of the article content from our test data and used python's yake package to extract keywords. Then, we ranked these results and used word2vec on each yake keyword and summed the vector similarity of any two words in the yake keywords for each article. We then multiplied this by the yake value and sorted the results from highest to lowest score. We placed the outputs on a new file

## Sections of the Code
### Document Extractor
This folder consists of a basic webscraper that uses user inputs to create documents with the text of different news sources. We are using this to develop our training, development, and test corpuses. The two files on this are clickLink.py, which extracts the text from each link that is parsed through using a selenium scraper. The newsAPIscraper.py file uses a news API to collect a set of sources using a query and a number of documents. It then develops the files for the corpuses used. 

### Corpuses
This folder consists of txt files with our training, dev, and test corpuses

### model
This folder contains our model in main2.py. It also inclides a data cleaner file to remove tags and odd spaces

### results
This folder contains our results
