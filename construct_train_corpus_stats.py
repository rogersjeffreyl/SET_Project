"""
used to analyze both the training and test corpus
"""
__author__ = 'rogersjeffrey'
import ddi_parser_corpus
#Disulfiram_ddi.xml
#paths=["/Users/rogersjeffrey/Downloads/DDICorpus/DDICorpus/Train/DrugBank","/Users/rogersjeffrey/Downloads/DDICorpus/DDICorpus/Train/Medline"]
paths=["./Test/Test for DDI Extraction task/DrugBank","./Test/Test for DDI Extraction task/Medline"]
corpus_analyzer_instance= ddi_parser_corpus.corpus_analyzer()
corpus_analyzer_instance.get_train_corpus_stats(paths)
