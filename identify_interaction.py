__author__ = 'rogersjeffrey'
'''
 classify the sentence as having positive or negative interaction   based on the bigrams
'''
import utils
import pprint
from collections import defaultdict
import cPickle as pickle
from xml.dom.minidom import parse

class indentify_interaction:
    def __init__(self):
        self.trigrams_based_on_score={}
        self.trigrams_based_on_occurence={}
        self.bigrams_based_on_score={}
        self.bigrams_based_on_occurence={}

    def load_model(self,file_list):

        self.trigrams_based_on_score=pickle.load(open(file_list[2],"rb"))
        self.trigrams_based_on_occurence=pickle.load(open(file_list[3],"rb"))
        self.bigrams_based_on_score=pickle.load(open(file_list[0],"rb"))
        self.bigrams_based_on_occurence=pickle.load(open(file_list[1],"rb"))
        #print self.bigrams_based_on_score
    def identify_interaction(self,path_to_test_file):

        document_data=open(path_to_test_file,'rb')
        xml_data=parse(document_data)
        sentences = xml_data.getElementsByTagName("sentence")
        result={}
        for sentence in sentences:
            entity_collection={}
            sentence_attrs = dict(sentence.attributes.items())
            sentence_text=sentence_attrs["text"]
            sentence_id=sentence_attrs["id"]
            entities = sentence.getElementsByTagName("entity")
            for entity in entities:
                    entity_attrs = dict(entity.attributes.items())
                    id=entity_attrs["id"]
                    text=(entity_attrs["text"]).lower()
                    type=(entity_attrs["type"]).lower()
                    entity_collection[id]={}
                    entity_collection[id]={"text":text,"type":type}
            words=utils.tokenize_string_without_punctuations(sentence_text)

            bigrams=utils.generate_bigrams(words)
            trigrams=utils.generate_trigrams(words)
            result_found=0

            for bigram in bigrams:

                if bigram in self.bigrams_based_on_score.keys():
                          result[sentence_id]={}
                          result[sentence_id]=self.bigrams_based_on_score[bigram]
                          result_found=1
                          print "bigram as a result of which classification is done:"+bigram
                          break
            if result_found!=1:
               result[sentence_id]="false"
        #pprint.pprint(self.bigrams_based_on_score)
        document_data.close()
        return  result