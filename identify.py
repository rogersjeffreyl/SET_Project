__author__ = 'rogersjeffrey'
'''
  use the heuristics to identify if the given sentence has a possible interaction or not
  and print the stats
'''
import  identify_interaction as id
import evaluator as evalu
import pprint
import utils
import  cPickle as pickle
id_instance=id.indentify_interaction()
eval_instance=evalu.evaluator()
files_list=["models/bigram_diff.p","models/bigram_diff_total.p","models/trigram_diff.p","models/trigram_diff_total.p"]
id_instance.load_model(files_list)
#paths=["/Users/rogersjeffrey/Downloads/DDICorpus/DDICorpus/Train/DrugBank","/Users/rogersjeffrey/Downloads/DDICorpus/DDICorpus/Train/Medline"]
paths=["./Test/Test for DDI Extraction task/DrugBank","./Test/Test for DDI Extraction task/Medline"]
files=utils.get_files_list(paths)

total_sentence_count=0
for file in files:
    result=id_instance.identify_interaction(file)
    for sentence_id in result:
        total_sentence_count+=1
        prediction=result[sentence_id]

        eval_instance.validate_on_train_data(sentence_id,prediction)
print "Sentence_count:%d" %total_sentence_count
print "TP:%d" %eval_instance.true_positive
print "TN:%d" %eval_instance.true_negative
print "FP:%d" %eval_instance.false_positive
print "FN:%d" %eval_instance.false_negative

precision=float(eval_instance.true_positive)/float(eval_instance.true_positive+eval_instance.false_positive)
recall=float(eval_instance.true_positive)/float(eval_instance.true_positive+eval_instance.false_negative)
f_score=2*precision*recall/(precision+recall)
print "Precision:%f"%precision
print "Recall:%f"%recall
print "Fscore:%f"%f_score



