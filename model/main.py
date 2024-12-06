"""
1. Create a function that tags the words in the cleaned data. 
2. Use CBOW from word2vec library to compute word embeddings - pip
3. use YAKE to extract yake keywords 
4. for each YAKE keyword, split each of the top 1000 keywords into adjectives and nouns. Place them into a list
5. TBD on implementation, use the word2vec graph to get the words closest in distance. Return top 20
TO DO: remove stopwords
"""

from gensim.models import Word2Vec
import pke 
import re
import dataCleaner as dc
import string
import nltk
from nltk.corpus import stopwords
from yake import KeywordExtractor
import numpy as np

class key:
    def __init__ (self):
        self.np = r'(DET)?(JJR?S?)*(NNP?S?)+'
        self.pn = r'(NNP)*'
        self.vb = r'(VBD?G?N?P?Z?)'
        self.jj = r'JJR?S?'
        self.vp = r'(IN)?(RBS?)*(VBD?G?N?P?Z?)(RBD?)'
        self.patterns = [self.np,self.pn,self.vb,self.jj,self.vp]
    def allPOS(self):
        return self.patterns


def yakeKeywords(KE,str):
    strArr = str.split("\n")
    allKeywords = []
    for entry in strArr:
        toAppend = KE.extract_keywords(entry)
        allKeywords.append(toAppend)


    return allKeywords

def isValid (wp):
    """
    Get 5 -15 keywords from the test, based on the following requirements
Up to  consecutive words unless long proper noun
No more than one entity
Noun phrase, proper name, verb, adj, phrasal verb, or part of clause
No full sentences, conjunctions, adverbs, determiner, number, preposition, or pronoun
No base form
Only one word for each concept

    """
    tokens = nltk.word_tokenize(wp)
    tagged_tokens = nltk.pos_tag(tokens)
    tags = ""
    keys = key()
    all = keys.allPOS()
    for item in tagged_tokens:
        tags +=item[1]
        for k in all:
            pattern = re.compile(k)
            if pattern.match(tags):
                return item
    return None

    


    




def main():
    #extractor = pke.unsupervised.YAKE()
    allText = dc.cleantext('../corpuses/training.txt')
    sentences = dc.splitLines(allText)
    sw = set(stopwords.words('english'))
    news_stopwords = set([
    "breaking", "news", "journal", "times", "post", "herald", "gazette", 
    "daily", "weekly", "monthly", "article", "editorial", "press", "media", 
    "report", "reporting", "publication", "columnist", "coverage", "network", 
    "wire", "agency", "source", "sources", "headline", "reuters", "associated", 
    "ap", "nytimes", "cnn", "bbc", "fox", "npr", "bloomberg", "politico", 
    "wsj", "guardian", "telegraph", "tribune"])
    combinedStopwords = sw.union(news_stopwords)
    sentences = [line.translate(str.maketrans('', '', string.punctuation)).split() for line in sentences]
    w2v = Word2Vec(sentences = sentences)
    KE = KeywordExtractor(stopwords=combinedStopwords)
    yakekeys = np.array(yakeKeywords(KE,allText),dtype = object)
    flat = [item for sublist in yakekeys for item in sublist]
    print(flat[1])
    rank = sorted(flat,key = lambda x:x[1])
    kw = {}
    w2vSims = {}
    indexArr = []
    
   # print(rank[:500])
    i=0
    rankNum =0
    while i<100 and rankNum<len(rank):
        p=rank[rankNum]
        if isValid(p[0]):
            kw[p[0]]=p[1]
            indexArr.append(p[0])
            i+=1
        rankNum+=1
    for i in indexArr:
        for j in indexArr:
            if i==j:
                continue
            else:
                if i in w2vSims.keys():
                    product = 0
                    indivWordsi = i.split()
                    indivwordsj = j.split()
                    for wordi in indivWordsi:
                        for wordj in indivwordsj:
                            if wordi == wordj: 
                                continue
                            elif wordi in w2v.wv.key_to_index and wordj in w2v.wv.key_to_index:
                                product += w2v.wv.similarity(wordi,wordj)
                            else:
                                continue


                    orig = w2vSims[i]
                    w2vSims[i] = orig+product
                else:
                    product = 0
                    indivWordsi = i.split()
                    indivwordsj = j.split()
                    for wordi in indivWordsi:
                        for wordj in indivwordsj:
                            if wordi == wordj:
                                continue
                            elif wordi in w2v.wv.key_to_index and wordj in w2v.wv.key_to_index:
                                product += w2v.wv.similarity(wordi,wordj)
                            else:
                                continue
                    w2vSims[i]=product
    rankwtv = sorted(w2vSims.items(), key=lambda x: x[1], reverse = True)
    print(rankwtv)

    
    
    
    






if __name__ == "__main__":
    main()