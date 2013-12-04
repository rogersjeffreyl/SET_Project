import utils
from collections import  defaultdict
from xml.dom.minidom import parse
import datetime
"""
 initial script needed to evaluate the  bigram heuristics we generate
"""

def evaluate_heuristics(paths):

    interaction_words=defaultdict(int)
    paths=utils.get_files_list(paths)
    entity_collection={}
    interaction_collection={}
    cue_words=[]
    with open("ddi_key_phrase") as key_data:
         for line in key_data:
             cue_words+=[line.strip()]
    with open("ddi_trigger") as key_data:
         for line in key_data:
             cue_words+=[line.strip()]
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
            #for word in cue_words:
                #if word in text
            entities = sentence.getElementsByTagName("entity")
            for entity in entities:
                entity_attrs = dict(entity.attributes.items())
                id=entity_attrs["id"]
                text=(entity_attrs["text"]).lower()
                type=(entity_attrs["type"]).lower()
                entity_collection[id]={}
                entity_collection[id]={"text":text,"type":type}

            document_data.close()

paths=["./Test/Test for DDI Extraction task/DrugBank","./Test/Test for DDI Extraction task/Medline"]
