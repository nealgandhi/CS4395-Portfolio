import nltk
from nltk.util import ngrams
import pickle


def ngramdict(filename):
    file_content = open(filename, encoding="utf-8").read()
    unigrams = nltk.word_tokenize(file_content)
    bigrams = list(ngrams(unigrams,2))
    bigram_dict = {b:bigrams.count(b) for b in set(bigrams)}
    unigram_dict = {t:unigrams.count(t) for t in set(unigrams)}
    return bigram_dict, unigram_dict



en_bigram_dict, en_unigram_dict = ngramdict("data/LangId.train.English")
fr_bigram_dict, fr_unigram_dict = ngramdict("data/LangId.train.French")
itl_bigram_dict, itl_unigram_dict = ngramdict("data/LangId.train.Italian")

with open('en_bigram.pkl', 'wb') as f:
    pickle.dump(en_bigram_dict, f)
with open('en_unigram.pkl', 'wb') as f:
    pickle.dump(en_unigram_dict, f)
with open('fr_bigram.pkl', 'wb') as f:
    pickle.dump(fr_bigram_dict, f)
with open('fr_unigram.pkl', 'wb') as f:
    pickle.dump(fr_unigram_dict, f)
with open('itl_bigram.pkl', 'wb') as f:
    pickle.dump(itl_bigram_dict, f)
with open('itl_unigram.pkl', 'wb') as f:
    pickle.dump(itl_unigram_dict, f)

