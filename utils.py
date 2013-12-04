__author__ = 'rogersjeffrey'
"""
has the utility scripts for generating bigrams trigrams and unigrams
"""
from os import listdir
from nltk.tokenize import RegexpTokenizer
import pprint

def construct_path(directory,file):

      if directory.endswith("/") or directory.endswith("\\"):
         return directory+file
      else:
         return  directory+"/"+file

#returns all the files in a path
#if path does not exist throws an exception
# if directory is empty it throws an exception
def get_files_in_path(path):
    files=None
    try:

     files= listdir(path)
     if files ==None:
        raise OSError
     return files

    except OSError:
     print "Invalid path.  Kindly enter a valid path to the corpus"
     raise SystemExit

def get_files_list(paths):
    total_files=[]
    for each_dir in paths:
        files=get_files_in_path(each_dir)
        for file in files:
            total_files.append(construct_path(each_dir,file))
    return total_files

def tokenize_string_without_punctuations(input_string):
    #tokenizer = RegexpTokenizer(r'(?<=)(?![0-9]+)(\w+[-]*(\w)*)')
    #tokenizer = RegexpTokenizer(r'(?<=)(?![0-9]+)(\w+)')
    tokenizer=RegexpTokenizer(r"(?<=)(?![0-9]+)(?!e\.)(?!g\.)(\w+[-]*(\w)*)")
    return tokenizer.tokenize(input_string)

def generate_bigrams(word_array):

    bigram_hash={}
    bigram_count=0
    bigram_end_index=1
    length=len(word_array)-1

    while bigram_end_index <length-1 and length>=1:
        first_word=word_array[bigram_count]
        second_word=word_array[bigram_count+1]
        bigram=str(first_word.lower())+","+str(second_word.lower())
        if bigram in bigram_hash.keys():
           bigram_count=bigram_count+1
           bigram_end_index=bigram_count+1
           continue
        else:
           bigram_hash[bigram]={}
           bigram_hash[bigram]=1

        bigram_count=bigram_count+1
        bigram_end_index=bigram_count+1
    return bigram_hash

def generate_trigrams(word_array):
    trigram_hash={}
    length=len(word_array)-1
    trigram_end_index=2
    trigram_count=0
    while trigram_end_index <=length-2 and length>=2:
        first_word=str(word_array[trigram_count].lower())
        second_word=str(word_array[trigram_count+1].lower())
        third_word=str(word_array[trigram_count+2].lower())
        trigram=first_word+","+second_word+","+third_word
        if trigram_hash.has_key(trigram):
           trigram_count=trigram_count+1
           trigram_end_index=trigram_count+2
           continue
        else:
           trigram_hash[trigram]={}
           trigram_hash[trigram]=1
        trigram_count=trigram_count+1
        trigram_end_index=trigram_count+2
    return trigram_hash

def generate_unigrams(word_array):
    unigram_hash={}
    length=len(word_array)-1
    unigram_count=0
    while unigram_count<=length:
        word=str(word_array[unigram_count].lower())
        if word in unigram_hash:
           unigram_count=unigram_count+1
           continue
        else:
           unigram_hash[word]={}
           unigram_hash[word]=1
        unigram_count=unigram_count+1
    return unigram_hash
