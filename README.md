# bert_output
Assumes the input is of the format
Label\tSpace-separated-tokens

if the input is one sentence per line, like the stanford sentiment treebank, pass the "--dont_split" flag to sentence_splitting.py. otherwise, it splits the data into sentences.

in reading_bert.py, concat_all_layers = False makes the BERT output be the sum of the last four layers' embeddings for each token, while concat_all_layers = True makes it the concatenation (so 4X as large). 
