'''used to view the stats if the document'''
__author__ = 'rogersjeffrey'
import cPickle as pickle
import  pprint
from sys import argv
def print_stats(type,corpus):

    doc_stats=pickle.load(open("models/"+corpus+"_"+type+"_stats.p"))

    for key1 in doc_stats:
        print key1,doc_stats[key1][0],doc_stats[key1][1],doc_stats[key1][2],doc_stats[key1][3],doc_stats[key1][4]


#print_stats("unigram")
#print_stats("bigram")
#print_stats("trigram")
(script_name,corpus,stats)=argv

print_stats(stats,corpus)
stats=pickle.load(open("./models/"+corpus+"_corpus_stats.p"))
print stats