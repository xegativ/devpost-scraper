# extractive summarization 
# - extracts several parts, such as phrases and sentences

import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter
from heapq import nlargest


class Summarize():

    def __init__(self, comn=10, text=""):
        # load nlp
        nlp = spacy.load('en_core_web_sm')

        # stored text rdy to summarize
        self.text = nlp(text)

        # freq_word, score based on top comn words
        self.comn = comn

    # update text that is being summarized/stored
    def setText(self, text=""):
        self.text = text

    # filters to most occuring words, scores top comn
    def filterTokens(self):
        keyword = []
        stopwords = list(STOP_WORDS)
        pos_tag = ['PROPN', 'ADJ', 'NOUN', 'VERB']
        for token in self.text:
            if(token.text in stopwords or token.text in punctuation):
                continue 
            if(token.pos_ in pos_tag):
                keyword.append(token.text)

        freq_word = Counter(keyword) 
        # freq_word.most_common(self.comn)

        # normalization
        max_freq = Counter(keyword).most_common(1)[0][1]
        for word in freq_word.keys():
            freq_word[word] = (freq_word[word]/max_freq)
        freq_word.most_common(self.comn)

        return freq_word
    
    # weighing sentences (only keeping most important)
    def sentenceWeigh(self, freq_word):
        sent_strength = {}
        for sent in self.text.sents:
            for word in sent:
                if word.text in freq_word.keys():
                    if sent in sent_strength.keys():
                        sent_strength[sent] += freq_word[word.text]
                    else:
                        sent_strength[sent] = freq_word[word.text]
        return sent_strength
    

    def summarize(self, n_sentences):
        sent_strength = self.sentenceWeigh(self.filterTokens())
        summarized_sentences = nlargest(n_sentences, sent_strength, key=sent_strength.get)

        final_sentences = [ w.text for w in summarized_sentences ]
        summary = ' '.join(final_sentences)
        return summary
