__author__ = 'rogersjeffrey'
"""
consturucts the model data from the statistics (chooses the number of trigrams and bigrams)
"""
import construct_training_model as tm
from sys import argv
import pprint
(script_name,bigram_count)=argv
training_model_instance=tm.training_model()
training_model_instance.generate_train_model(int(bigram_count),-1,"stats/bigram_diff.txt",1)
training_model_instance.generate_train_model(-1,-1,"stats/bigram_diff_total.txt",2)
training_model_instance.generate_train_model(-1,-1,"stats/trigram_diff.txt",3)
training_model_instance.generate_train_model(-1,-1,"stats/trigram_diff_total.txt",4)