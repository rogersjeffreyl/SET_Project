__author__ = 'rogersjeffrey'
"""
  use to evaluate the runs on the test data
"""
import utils
import pprint
from collections import defaultdict
from xml.dom.minidom import parse, parseString

import cPickle as pickle

class evaluator:

    def __init__(self):
        self.train_sentence_model=pickle.load(open("models/test_sentence_stats.p","rb"))
        self.total_correct=0
        self.total_incorrect=0
        self.true_positive=0
        self.false_positive=0
        self.true_negative=0
        self.false_negative=0
        self.true_positives=[]
        self.false_positives=[]
        self.true_negatives=[]
        self.false_negatives=[]
        #pprint.pprint(self.train_sentence_model)

    def validate_on_train_data(self,sentence_id,prediction):

        # True positive

        if self.train_sentence_model[sentence_id]=="true" and prediction=="true":
             self.total_correct+=1
             self.true_positive+=1
             self.true_positives+=[sentence_id]
        # False Positive
        elif self.train_sentence_model[sentence_id]=="false" and prediction=="true":
             self.total_incorrect+=1
             self.false_positive+=1
             self.false_positives+=[sentence_id]
        # False negative
        elif self.train_sentence_model[sentence_id]=="true" and prediction=="false":
             self.total_incorrect+=1
             self.false_negative+=1
             self.false_negatives+=[sentence_id]
        #Correct negative classification
        elif self.train_sentence_model[sentence_id]=="false" and prediction=="false":
             self.true_negatives+=[sentence_id]
             self.total_correct+=1
             self.true_negative+=1
    def validate_prediction(self,predict_file):

        interaction_collection=pickle.load(open("models/test_data.p","rb"))
        #pprint.pprint(interaction_collection["DDI-DrugBank.d654"])
        correct_prediction_count=0
        total_count=0
        true_positive=0
        false_positive=0
        false_negative=0
        with open(predict_file) as predict_data:
            for line in predict_data:
                total_count=total_count+1
                if line.strip():
                    data=line.split("|")
                    document_id=data[0].split(".s")
                    is_ddi=None
                    if int(data[3])==0:
                        is_ddi="false"
                    elif int(data[3])==1:
                        is_ddi="true"

                    gold_data_answer=interaction_collection [document_id[0]] [data[0]][data[1]][data[2]]["ddi"]
                    gold_data_class=interaction_collection [document_id[0]] [data[0]][data[1]][data[2]]["type"]

                    if gold_data_class==None:
                        gold_data_class="null"
                        #print gold_data_class
                    #print data[4].strip()
                    #print gold_data_class==data[4].strip()
                    #print "\n"
                    if gold_data_answer==is_ddi:

                        if gold_data_class==data[4].strip():
                            correct_prediction_count+=1
                            if is_ddi=="true":
                                true_positive+=1
                                #print "correct_prediction:%d" %(correct_prediction_count)
                    else:
                        if gold_data_answer=="false" and is_ddi=="true":
                            false_positive+=1
                        elif gold_data_answer=="true" and is_ddi=="false":
                            false_negative+=1
        print float(correct_prediction_count)/float(total_count)
        precision=float(true_positive)/(true_positive+false_positive)
        recall=float(true_positive)/(true_positive+false_negative)
        f_score=(2*precision*recall)/(precision+recall)
        print "Precision:%f" %(precision)
        print "Recall:%f" %(recall)
        print "F-Score:%f" %(float(f_score))

    def print_corpus_stats(self,data_hash):
        counts={"true":0,"false":0,"mechanism":0,"int":0,"effect":0,"advise":0}
        for documents in data_hash:
            for sentences in data_hash[documents]:

                    for first_pair in data_hash[documents][sentences]:
                        for second_pair in data_hash[documents][sentences][first_pair]:
                            if data_hash[documents][sentences][first_pair][second_pair]["ddi"]=="true":
                               type=data_hash[documents][sentences][first_pair][second_pair]["type"]
                               counts[type]=counts[type]+1
                               counts["true"]=counts["true"]+1
                            else:
                               counts["false"]=counts["false"]+1
        return counts

    def parse_gold_annotation(self,paths):
        interaction_words=defaultdict(int)
        paths=utils.get_files_list(paths)
        entity_collection={}
        interaction_collection={}
        for file in paths:

            document_data=open(file,'r')
            xml_data=parse(document_data)
            document_elt= xml_data.getElementsByTagName("document")

            document_attrs=dict(document_elt[0].attributes.items())
            document_id=document_attrs["id"]

            sentences = xml_data.getElementsByTagName("sentence")

            for sentence in sentences:
                entity_collection={}
                sentence_attrs = dict(sentence.attributes.items())
                text=sentence_attrs["text"]
                entities = sentence.getElementsByTagName("entity")
                for entity in entities:
                    entity_attrs = dict(entity.attributes.items())
                    id=entity_attrs["id"]
                    text=(entity_attrs["text"]).lower()
                    type=(entity_attrs["type"]).lower()
                    entity_collection[id]={}
                    entity_collection[id]={"text":text,"type":type}

                interacting_pairs = sentence.getElementsByTagName("pair")
                for pair in interacting_pairs:
                        pair_attrs = dict(pair.attributes.items())
                        type=None
                        if pair_attrs.has_key("type"):
                           type=pair_attrs["type"]
                        if document_id not in interaction_collection.keys():
                           interaction_collection[document_id]={}
                        if sentence_attrs["id"] not in interaction_collection[document_id].keys():
                           interaction_collection[document_id][sentence_attrs["id"]] ={}
                        #if pair_attrs["id"] not in interaction_collection[document_id][sentence_attrs["id"]].keys():
                        #   interaction_collection[document_id][sentence_attrs["id"]][pair_attrs["id"]]={}
                        if pair_attrs["e1"] not in  interaction_collection[document_id][sentence_attrs["id"]].keys():
                           interaction_collection[document_id][sentence_attrs["id"]][pair_attrs["e1"] ]={}
                        if pair_attrs["e2"] not in  interaction_collection[document_id][sentence_attrs["id"]][pair_attrs["e1"]]:
                           interaction_collection[document_id][sentence_attrs["id"]][pair_attrs["e1"]][pair_attrs["e2"]]={}
                           interaction_collection[document_id][sentence_attrs["id"]][pair_attrs["e1"]][pair_attrs["e2"]]={"ddi":pair_attrs["ddi"],"type":type}
                document_data.close()
                pickle.dump(interaction_collection,open("models/test_data.p","wb"))
        #pprint.pprint(self.print_corpus_stats(interaction_collection))
