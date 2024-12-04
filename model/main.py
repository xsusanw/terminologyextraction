"""
1. Create a function that tags the words in the cleaned data. 
2. Use CBOW from word2vec library to compute word embeddings - pip
3. use YAKE to extract yake keywords 
4. for each YAKE keyword, split each of the top 1000 keywords into adjectives and nouns. Place them into a list
5. TBD on implementation, use the word2vec graph to get the words closest in distance. Return top 20
"""

from gensim.models import Word2Vec
import pke 
import re
import dataCleaner as dc
import string
from yake import KeywordExtractor
import numpy as np

def yakeKeywords(KE,str):
    strArr = str.split("\n")
    allKeywords = []
    for entry in strArr:
        toAppend = KE.extract_keywords(entry)
        allKeywords.append(toAppend)


    return allKeywords



def main():
    #extractor = pke.unsupervised.YAKE()
    allText = dc.cleantext('../corpuses/training.txt')
    sentences = dc.splitLines(allText)
    sentences = [line.translate(str.maketrans('', '', string.punctuation)).split() for line in sentences]
    w2v = Word2Vec(sentences = sentences)
    KE = KeywordExtractor()
    kw = np.array(yakeKeywords(KE,allText),dtype = object)
    flat = [item for sublist in kw for item in sublist]
    print(flat[1])
    rank = sorted(flat,key = lambda x:x[1],reverse=True)
    print(rank[:500])



if __name__ == "__main__":
    main()