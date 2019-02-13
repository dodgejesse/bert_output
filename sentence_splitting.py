import argparse
import spacy

def main():
    parser = argparse.ArgumentParser()

    ## Required parameters
    parser.add_argument("--input_file", default=None, type=str, required=True)
    parser.add_argument("--output_file", default=None, type=str, required=True)

    parser.add_argument("--dont_split", action="store_true")
    
    args = parser.parse_args()
    lines = read_file(args.input_file)

    if args.dont_split:
        print_sentences(lines, args.output_file)
    else:
        print_split_sentences(lines, args.output_file)

# for datasets that are already one sentence per example
def print_sentences(lines, output_file):
    with open(output_file, "w") as f:
        for line in lines:
            f.write(line + "\n")

# for datasets that have multiple sentences per example
def print_split_sentences(lines, output_file):
    nlp = spacy.load('en')
    with open(output_file, "w") as f:
        for line in lines:
            doc = nlp(line)

            for sent in doc.sents:
                f.write(str(sent).strip() + "\n")
            f.write("\n")
        
def read_file(file_loc):
    with open(file_loc) as f:
        data = f.readlines()

    return data
        
if __name__ == "__main__":
    main()
