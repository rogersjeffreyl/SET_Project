"""
Used to obtain information about test data files
"""
__author__ = 'rogersjeffrey'
import utils
import pprint
from xml.dom.minidom import parse, parseString
import  cPickle as pickle
class test_corpus:
   def __init__(self):
          self.entity_collection={}
          self.interaction_collection={}
          self.pairs_collection={}
          self.total_sentence_count=0
   def parse_ddi_corpus(self,file):

        #print file
        document_data=open(file,'r')
        xml_data=parse(document_data)
        sentences = xml_data.getElementsByTagName("sentence")

        for sentence in sentences:
            self.total_sentence_count+=1
            sentence_attrs = dict(sentence.attributes.items())
            text=sentence_attrs["text"]
            sentence_id=sentence_attrs["id"]
            words=utils.tokenize_string_without_punctuations(text)
            entities = sentence.getElementsByTagName("entity")
            for entity in entities:
                entity_attrs = dict(entity.attributes.items())
                id=entity_attrs["id"]
                text=(entity_attrs["text"]).lower()
                type=(entity_attrs["type"]).lower()
                self.entity_collection[id]={}
                self.entity_collection[id]={"text":text,"type":type}

            interacting_pairs = sentence.getElementsByTagName("pair")
            # removing drugs
            for ids in self.entity_collection:

                        if self.entity_collection[ids]["text"] in words:
                           words.remove(self.entity_collection[ids]["text"])

            for pair in interacting_pairs:
                pair_attrs = dict(pair.attributes.items())
                type="null"
                ddi="0"
                if "ddi" in pair_attrs.keys():
                    ddi=pair_attrs["ddi"]
                    if ddi=="false":
                       ddi="0"
                    elif ddi=="true":
                       ddi="1"

                if "type" in pair_attrs.keys():
                    type=pair_attrs["type"]

                #self.pairs_collection[pair_attrs["id"]]={}
                pair_id=pair_attrs["id"]
                self.pairs_collection[pair_id]=ddi

                entity_1=self.entity_collection[pair_attrs["e1"]]["text"]
                entity_2=self.entity_collection[pair_attrs["e2"]]["text"]

                if entity_1 in self.interaction_collection.keys():
                    if entity_2 not in self.interaction_collection[entity_1].keys():
                        self.interaction_collection[entity_1][entity_2]=ddi
                elif entity_2 in self.interaction_collection.keys():
                    if entity_1 not in self.interaction_collection[entity_2]:
                        self.interaction_collection[entity_2][entity_1]=ddi
                else:
                    self.interaction_collection[entity_2]={}
                    self.interaction_collection[entity_2][entity_1]=ddi
                    self.interaction_collection[entity_2][entity_1]=ddi


        document_data.close()
test_medline_path= "./Test/Test for DDI Extraction task/MedLine"
test_drugbank_path= "./Test/Test for DDI Extraction task/DrugBank"
paths=[test_medline_path,test_drugbank_path]
paths=utils.get_files_list(paths)
test_corpus_instance=test_corpus()
for file in paths:

    test_corpus_instance.parse_ddi_corpus(file)

    pickle.dump(test_corpus_instance.entity_collection,open("./models/test_entity_collection.p","wb"))
    pickle.dump(test_corpus_instance.interaction_collection,open("./models/test_interaction_collection.p","wb"))
    pickle.dump(test_corpus_instance.pairs_collection,open("./models/test_pairs_collection.p","wb"))
pprint.pprint(test_corpus_instance.pairs_collection)