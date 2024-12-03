"""
1. Create a function that tags the words in the cleaned data. 
2. Use CBOW from word2vec library to compute word embeddings - https://medium.com/@manansuri/a-dummys-guide-to-word2vec-456444f3c673
3. use YAKE to extract yake keywords 
4. for each YAKE keyword, split each of the top 1000 keywords into adjectives and nouns. Place them into a list
5. TBD on implementation, use the word2vec graph to get the words closest in distance. Return top 20
"""