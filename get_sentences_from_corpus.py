__author__ = 'rogersjeffrey'
"""
 This tool extracts all the  sentences from the test and the training corpus(both medline and drugbank)
 and stores them in separate directories (test_sentences and train_sentences)

"""
from xml.dom.minidom import parse
import utils
def write_sentences_to_file(input_file,write_path):
        document_data=open(input_file,'r')
        print input_file
        xml_data=parse(document_data)
        sentences = xml_data.getElementsByTagName("sentence")

        for sentence in sentences:

            sentence_attrs = dict(sentence.attributes.items())
            text=sentence_attrs["text"]
            sentence_id=sentence_attrs["id"]
            path=utils.construct_path(write_path,sentence_id)
            output_file=open(path,'w')
            output_file.write(text)
            output_file.close()


test_medline_path= "./Test/Test for DDI Extraction task/MedLine"
test_drugbank_path= "./Test/Test for DDI Extraction task/DrugBank"
train_medline_path="./Train/MedLine"
train_drugbank_path="./Train/DrugBank"

test_medline_path_files=utils.get_files_in_path(test_medline_path)
test_drugbank_path_files=utils.get_files_in_path(test_drugbank_path)
train_medline_path_files=utils.get_files_in_path(train_medline_path)
train_drugbank_path_files=utils.get_files_in_path(train_drugbank_path)

for file in test_drugbank_path_files:
    file=utils.construct_path(test_drugbank_path,file)
    write_sentences_to_file(file,"./test_sentences")
for file in test_medline_path_files:
    file=utils.construct_path(test_medline_path,file)
    write_sentences_to_file(file,"./test_sentences")
for file in train_drugbank_path_files:
    file=utils.construct_path(train_drugbank_path,file)
    write_sentences_to_file(file,"./train_sentences")
for file in train_drugbank_path_files:
    file=utils.construct_path(train_drugbank_path,file)
    write_sentences_to_file(file,"./train_sentences")



