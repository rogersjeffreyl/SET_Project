__author__ = 'rogersjeffrey'
from collections import defaultdict
from xml.dom.minidom import parse, parseString
import pprint
import utils
import  math
import cPickle as pickle
class corpus_analyzer:

    def __init__(self):

      #Unigrams
      self.interaction_true_word_count={}
      self.interaction_false_word_count={}

      #Bigrams
      self.interaction_true_bigram_count={}
      self.interaction_false_bigram_count={}

      # Trigrams
      self.interaction_true_trigram_count={}
      self.interaction_false_trigram_count={}

      #for the word counts
      self.total_sentence_count=0
      self.positive_sentence_count=0
      self.negative_sentence_count=0

      # Colelcting the interacting entities
      self.entity_collection={}
      self.interaction_collection={}

      #interaction information in sentences:
      self.sentence_interaction_information={}

    def populate_unigram_hashes(self,words,hash):
        unigrams=utils.generate_unigrams(words)
        for word in unigrams:

            if word  in hash.keys():
               hash[word]+=1
            else:
               hash[word]={}
               hash[word]=1

    def parse_character_offsets(character_offsets):
        character_offsets=character_offsets.split(";")
        for character_offset in character_offsets:
            end_of_offset=character_offset.split("-")
            print end_of_offset
    #def get_interaction_sentences:
    def update_trigram_hash(self,word_array,trigram_hash):

        trigrams=utils.generate_trigrams(word_array)
        for key in trigrams:
            if  key in trigram_hash.keys():
              trigram_hash[key]+=1
            else:
                trigram_hash[key]={}
                trigram_hash[key]=1
    def update_bigram_hash(self,word_array,bigrams_hash):
        bigrams=utils.generate_bigrams(word_array)
        for key in bigrams:
            if  key in bigrams_hash.keys():
              bigrams_hash[key]+=1
            else:
                bigrams_hash[key]={}
                bigrams_hash[key]=1

    def parse_ddi_corpus(self,file):

        #print file
        document_data=open(file,'r')
        xml_data=parse(document_data)
        sentences = xml_data.getElementsByTagName("sentence")

        for sentence in sentences:
            # setting flag to zero at the beginning of sentence
            is_there_a_positive_interaction_for_sentence=0
            is_there_a_negative_interaction_for_sentence=0
            #counting the total sentences
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

                if "type" in pair_attrs.keys():
                    type=pair_attrs["type"]

                if pair_attrs["ddi"]=="true":
                    is_there_a_positive_interaction_for_sentence=1

                    entity_1=self.entity_collection[pair_attrs["e1"]]["text"]
                    entity_2=self.entity_collection[pair_attrs["e2"]]["text"]

                    if entity_1 in self.interaction_collection.keys():
                        if entity_2 not in self.interaction_collection[entity_1].keys():
                            self.interaction_collection[entity_1][entity_2]=type
                    elif entity_2 in self.interaction_collection.keys():
                        if entity_1 not in self.interaction_collection[entity_2]:
                            self.interaction_collection[entity_2][entity_1]=type
                    else:
                        self.interaction_collection[entity_2]={}
                        self.interaction_collection[entity_2][entity_1]=type
                elif pair_attrs["ddi"]=="false" and is_there_a_positive_interaction_for_sentence!=1:
                     is_there_a_negative_interaction_for_sentence=1
            if is_there_a_positive_interaction_for_sentence ==1:
                    self.sentence_interaction_information[sentence_id]={}
                    self.sentence_interaction_information[sentence_id]="true"
                    self.positive_sentence_count=self.positive_sentence_count+1
                    self.populate_unigram_hashes(words,self.interaction_true_word_count)
                    self.update_bigram_hash(words,self.interaction_true_bigram_count)
                    self.update_trigram_hash(words,self.interaction_true_trigram_count)
            elif is_there_a_negative_interaction_for_sentence==1:
                   self.negative_sentence_count=self.negative_sentence_count+1
                   self.populate_unigram_hashes(words,self.interaction_false_word_count)
                   self.update_bigram_hash(words,self.interaction_false_bigram_count)
                   self.update_trigram_hash(words,self.interaction_false_trigram_count)
                   self.sentence_interaction_information[sentence_id]={}
                   self.sentence_interaction_information[sentence_id]="false"
            else:
                   self.sentence_interaction_information[sentence_id]={}
                   self.sentence_interaction_information[sentence_id]="false"
        document_data.close()

    def get_hash_stats(self,positive_hash,negative_hash):
        stats={}
        for keys in positive_hash:
            positive_count=positive_hash[keys]
            negative_count=0
            if keys in negative_hash:
               negative_count=negative_hash[keys]
            total_count=positive_count+negative_count
            diff=positive_count-negative_count
            stats[keys]=(float(abs(diff))/float(total_count),float(abs(diff))/float(self.total_sentence_count),positive_count,negative_count,diff)
        for keys in negative_hash:
            negative_count=negative_hash[keys]
            if keys in positive_hash.keys():
               continue
            else:
               total_count=negative_count
               diff=0-negative_count
               stats[keys]=(float(abs(diff))/float(total_count),float(abs(diff))/float(self.total_sentence_count),0,negative_count,diff)
        return stats

    def get_train_corpus_stats(self,paths):



         paths=utils.get_files_list(paths)
         for file in paths:
             self.parse_ddi_corpus(file)

         unigram_stats=self.get_hash_stats(self.interaction_true_word_count,self.interaction_false_word_count)
         bigram_stats=self.get_hash_stats(self.interaction_true_bigram_count,self.interaction_false_bigram_count)
         trigram_stats=self.get_hash_stats(self.interaction_true_trigram_count,self.interaction_false_trigram_count)

         pickle.dump(unigram_stats,open("models/train_unigram_stats.p",'wb'))
         pickle.dump(bigram_stats,open("models/train_bigram_stats.p",'wb'))
         pickle.dump(trigram_stats,open("models/train_trigram_stats.p",'wb'))
         pickle.dump(self.sentence_interaction_information,open("models/sentence_stats.p",'wb'))

         corpus_stats={}
         corpus_stats["positive_sentences"]=self.positive_sentence_count
         corpus_stats["negative_sentences"]=self.negative_sentence_count
         corpus_stats["total_sentences"]=self.total_sentence_count

         pickle.dump(corpus_stats,open("models/train_corpus_stats.p",'wb'))