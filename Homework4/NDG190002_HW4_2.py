import pickle
import nltk
from nltk.util import ngrams

def compute_probability(text, uni_dict, bi_dict, V):
    # using LaPlace smoothing to find maximum likelihood estimate
    unigrams_test = nltk.word_tokenize(text)
    bigrams_test = list(ngrams(unigrams_test, 2))
    p_laplace = 1
    for bigram in bigrams_test:
        n = bi_dict[bigram] if bigram in bi_dict else 0
        d = uni_dict[bigram[0]] if bigram[0] in uni_dict else 0

        p_laplace = p_laplace * ((n + 1) / (d + V))

    return p_laplace


def main():
    # read pickles
    en_bigram_dict = pickle.load(open('en_bigram.pkl', 'rb'))
    en_unigram_dict = pickle.load(open('en_unigram.pkl', 'rb'))
    fr_bigram_dict = pickle.load(open('fr_bigram.pkl', 'rb'))
    fr_unigram_dict = pickle.load(open('fr_unigram.pkl', 'rb'))
    itl_bigram_dict = pickle.load(open('itl_bigram.pkl', 'rb'))
    itl_unigram_dict = pickle.load(open('itl_unigram.pkl', 'rb'))
   # process test file
    with open('LangId.test', 'r') as f:
        text_in = f.readlines()

    # define V (vocabulary size) for each language
    en_V = len(en_unigram_dict)
    fr_V = len(fr_unigram_dict)
    itl_V = len(itl_unigram_dict)

    # stuffs
    line_no = 1
    output = open('accuracy.txt', 'w')
    with open('LangId.sol', 'r') as s:
        solution = s.readlines()
    wrong = []

    # compute the highest language probability for lines in test file
    for line in text_in:
        en_prob = compute_probability(line, en_unigram_dict, en_bigram_dict, en_V)
        fr_prob = compute_probability(line, fr_unigram_dict, fr_bigram_dict, fr_V)
        itl_prob = compute_probability(line, itl_unigram_dict, itl_bigram_dict, itl_V)
        best = max(en_prob, fr_prob, itl_prob)
        if best == en_prob:
            language = "English"
        elif best == fr_prob:
            language = "French"
        else:
            language = "Italian"
        
        # output guess
        string = str(line_no) + " " + language + "\n"
        output.write(string)

        if string != solution[line_no - 1]:
            wrong.append(str(line_no))

        line_no += 1

    # output accuracy stats
    accuracy = (line_no - len(wrong)) / line_no
    accuracy_percent = round(accuracy * 100, 2)
    string = "Accuracy (as percentage of correctly classified sentences in test set): " + str(accuracy) + " or " + str(
        accuracy_percent) + "%\n"
    output.write(string)

    string = "Line numbers of incorrectly classified sentences: " + ','.join(wrong)
    output.write(string)


if __name__ == '__main__':
    main()