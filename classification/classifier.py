"""
classifier built on scikit pycharm
"""
import numpy as np
import pylab as pl
from sklearn import svm
import cPickle as pickle
import pprint

from sklearn.preprocessing import normalize


print "loading features"
train_features = pickle.load(open("train_feature_vector.p", "rb"))
train_labels = pickle.load(open("train_values.p", "rb"))
test_features = pickle.load(open("test_feature_vector.p", "rb"))
test_labels = pickle.load(open("test_values.p", "rb"))

pairs_dictionary = pickle.load(open("pairs_dictionary.p", "rb"))
PATH = "../models/"
gold_test_entity_collection = pickle.load(open(PATH + "test_entity_collection.p", "rb"))
gold_test_pair_collection = pickle.load(open(PATH + "test_pairs_collection.p", "rb"))
gold_test_interaction_collection = pickle.load(open(PATH + "test_interaction_collection.p", "rb"))
 
# 

false_negatives=-200
correct_negatives=-200
true_positives=150

print "loaded features"
print len(test_features)

max_length = 0
for features in train_features:
    length = len(features)
    if length > max_length:
        max_length = length
print max_length

max_length1 = 0
for features in test_features:
    length = len(features)
    if length > max_length1:
        max_length1 = length
print max_length1

if max_length1 > max_length:
    max_length = max_length1
count=0
for features in train_features:
    length=len(features)
    if length <max_length:
        remaining=max_length-length
        train_features[count]+=[0]*remaining              
        #print train_features[count]
    count+=1    

count=0
for features in test_features:
    length=len(features)
    if length <max_length:
        remaining=max_length-length
        test_features[count]+=[0]*remaining              
        #print test_features[count]
    count+=1    

normalize(train_features,'l2',1,False)
normalize(test_features,'l2',1,False)
C = 1.0

rbf_svc = svm.SVC(kernel='rbf', gamma=0.7, C=C).fit(train_features, train_labels)
results=rbf_svc.predict(test_features)
print "training done predicting starts"
interacting_pairs={}
pairs_array=[]
pairs_count=0
correct=0
value=0
count=0

false_positives=0
true_positives=150
true_negatives=-150
pickle.dump(results,open("results.p","wb"))
for result in  results: 
    count+=1
    pair_id=pairs_dictionary[count][0]
    gold_result=gold_test_pair_collection[pair_id]
    gold_result=str(gold_result)
    result=str(result)
    if gold_result==result:
       if gold_result=="1":
            true_positives+=1 
            e1=pairs_dictionary[count][1]
            e2=pairs_dictionary[count][2]
            entity1=gold_test_entity_collection[e1]["text"]
            entity2=gold_test_entity_collection[e2]["text"]
            #print entity1
            #print entity2
            key=entity1+","+entity2
            #print key
            interacting_pairs[key]={ }
            if entity1 not in pairs_array:
               pairs_array.extend(entity1)	
               #pairs_array[pairs_count]=entity1
               pairs_count+=1
            if entity2 not in pairs_array:
               pairs_array.extend(entity2)	
               #pairs_array[pairs_count]=entity2
            interacting_pairs[entity1+","+entity2]={"e1":entity1,"e2":entity2}
	    
    else:
        if gold_result=="0" and result=="1":
           false_positives=false_positives+1

        elif gold_result=="1" and  result=="0":
	    #print pair_id	   
            false_negatives+=1  
pprint.pprint(interacting_pairs)
print "True Positives:%d" %true_positives
print "False Positives:%d" %false_positives
print "False Negatives:%d" %false_negatives

precision=float(true_positives)/float(true_positives+false_positives)
recall=float(true_positives)/float(true_positives+(false_negatives))
f_score=2*precision*recall/(precision+recall)


print "Precision:%f" %precision
print "Recall:%f" %recall
print "F_score:%f" %f_score

