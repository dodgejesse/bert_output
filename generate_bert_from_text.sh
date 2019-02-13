# with conda activate pytorch-pretrained-BERT
# and after splitting data into sentences. the split data should be stored in e.g. train_tokens files.
DATA_LOCATION=/home/jessedd/data/bert/sst

for DATA_SPLIT in dev train test; do
    DATA=${DATA_LOCATION}/${DATA_SPLIT}
    echo "creating docs without labes..."
    cat ${DATA} | awk '{$1=""; print $0}' > ${DATA}_docs
    cat ${DATA} | awk '{print $1}' > ${DATA}_labels
    echo "done creating file without labels, now splitting docs into sentences..."
    python sentence_splitting.py --input_file ${DATA}_docs --output_file ${DATA}_sentences --dont_split
    echo "done splitting docs into sentences, now generating bert embeddings..."
    python /home/jessedd/projects/pytorch-pretrained-BERT/examples/extract_features.py --input_file ${DATA}_sentences --output_file ${DATA}_bert_all --bert_model bert-large-uncased --do_lower_case
    echo "done generating bert contextualized representation for each word piece, now extracting just the embeddings..."
    python reading_bert.py --input_file ${DATA}_bert_all --output_file ${DATA}_bert_concat
    echo "done extracting the embeddings, now combining with the label..."
    paste ${DATA}_labels ${DATA}_bert_concat > ${DATA}_bert
    rm ${DATA}_docs ${DATA}_labels ${DATA}_sentences ${DATA}_bert_all ${DATA}_bert_concat
    echo "done! the bert embeddings are stored in the *_bert file."
done
