# file location: /home/jessedd/projects/pytorch-pretrained-BERT/samples/sample_text_output.txt

import json
import argparse
import numpy as np

def main():
    parser = argparse.ArgumentParser()

    ## Required parameters
    parser.add_argument("--input_file", default=None, type=str, required=True)
    parser.add_argument("--output_file", default=None, type=str, required=True)

    args = parser.parse_args()

    #args.input_file = "/home/jessedd/data/bert/amazon_categories/debug/dev_bert"
    #args.input_file = "/home/jessedd/projects/pytorch-pretrained-BERT/samples/sample_text_output.txt"
    
    with open(args.input_file) as f:
        data = f.readlines()
        
    tmp = json.loads(data[1])

    examples = get_examples(data)

    save_examples(examples, args.output_file)
    
    # ran this, and found that yes, all blank lines have the same embeddings
    #check_all_blank_lines_same(data)


def save_examples(examples, output_file):
    with open(output_file, "w") as f:
        for ex in examples:
            f.write(str(ex) + "\n")

def get_examples(data):
    examples = []
    cur_example = []
    for i in range(len(data)):
        cur_line = json.loads(data[i])
        # a blank line has two features, and denotes the delimiter between examples
        if len(cur_line['features']) == 2:
            examples.append(cur_example)
            cur_example = []
        # loop over the tokens in one sentence
        else:
            for j in range(len(cur_line['features'])):

                # when concat_all_layers == False, it sums layers. otherwise it concats them.
                concat_all_layers = False
                if concat_all_layers:
                    cur_embedding = []
                    
                    for k in range(len(cur_line['features'][j]['layers'])):
                        cur_embedding.extend(cur_line['features'][j]['layers'][k]['values'])
                    cur_example.append(cur_embedding)
                else:
                    cur_embedding = np.asarray(cur_line['features'][j]['layers'][0]['values'])
                    
                    for k in range(1, len(cur_line['features'][j]['layers'])):
                        cur_embedding += np.asarray(cur_line['features'][j]['layers'][k]['values'])
                    
                    cur_example.append(cur_embedding.round(decimals=6).tolist())
                    
    return examples
    
# it is true that the first 5 dimensions of the [CLS] marker for blank lines is the same, so i'm assuming the entire embedding is.
def check_all_blank_lines_same(data):
    for i in range(len(data)):
        cur_line = json.loads(data[i])
        if len(cur_line['features']) == 2:
            print(cur_line['features'][0]['layers'][0]['values'][0:5])
            import pdb; pdb.set_trace()

    

if __name__ == "__main__":
    main()


    







