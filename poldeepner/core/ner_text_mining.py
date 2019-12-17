import nltk, re, pprint
import glob
from nltk import word_tokenize 

from poldeepner import PolDeepNer
from process_poleval import align_tokens_to_text
from utils import wrap_annotations

nltk.download('punkt')

ner = PolDeepNer("model")


# Take all files from directory
RESULT_FILE = 'result.csv'
PATH = './text/'
files = glob.glob(PATH+'/**/*', recursive=True)
for file in files:
    try:
        with open(file, encoding='utf-8') as f:
            for sentences in f.readlines():
                sent_text = sentences#nltk.sent_tokenize(sentences)
                text = sent_text.strip().replace("\"", "'").replace("''"," '")
                tokens = word_tokenize(text)
                labels = ner.process_sentence(tokens)
                offsets = align_tokens_to_text([tokens], text)

                for an in wrap_annotations([labels]):
                    if an.annotation == "persName":
                        begin = offsets[an.token_ids[0]][0]
                        end = offsets[an.token_ids[-1]][1]
                        orth = sentences[begin:end]
                        print(f"{begin}:{end};{orth};{file}")
    except Exception as e:
        pass
        #print(f"Exception for {file}:")
        #print(e)