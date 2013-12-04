__author__ = 'rogersjeffrey'
"""
  generates the training model by storing the information about corpus inot pickle files
"""
import cPickle as pickle
class training_model:
    def __init__(self):
        self.trigrams_based_on_score={}
        self.trigrams_based_on_occurence={}
        self.bigrams_based_on_score={}
        self.bigrams_based_on_occurence={}


    def populate_hash(self,threshold_number_of_records,threshold_probability,file,hash):
        count=0
        with open(file,'r') as data :
              for line in data:
                  count=count+1
                  values=line.strip().split()
                  if threshold_number_of_records > -1:
                     if count>threshold_number_of_records:
                         break
                  if threshold_probability > -1:
                     if float(values[2])<threshold_probability:
                        break


                  pos_or_neg=None
                  if int(values[len(values)-1])<0:
                     pos_or_neg="false"
                  else:
                      pos_or_neg="true"
                  hash[values[0]]={}
                  hash[values[0]]=pos_or_neg

    def generate_train_model(self,threshold_number_of_records,threshold_probability,file,type):
        file_names=file.split("/")
        file_name=file_names[len(file_names)-1].split(".")[0]
        file_name="models/"+file_name
        if type==1:
           #Bigrams based on score
           self.populate_hash(threshold_number_of_records,threshold_probability,file,self.bigrams_based_on_score)
           pickle. dump(self.bigrams_based_on_score,open(file_name+".p","wb"))
        elif type==2:
           # Bigrams based on occurence
           self.populate_hash(threshold_number_of_records,threshold_probability,file,self.bigrams_based_on_occurence)
           pickle. dump(self.bigrams_based_on_occurence,open(file_name+".p","wb"))
        elif type==3:
           #Trigrams based on score
            self.populate_hash(threshold_number_of_records,threshold_probability,file,self.trigrams_based_on_score)
            pickle. dump(self.trigrams_based_on_score,open(file_name+".p","wb"))
        elif type==4:
           #Trigrams based on occurence
            self.populate_hash(threshold_number_of_records,threshold_probability,file,self.trigrams_based_on_occurence)
            pickle. dump(self.trigrams_based_on_occurence,open(file_name+".p","wb"))


