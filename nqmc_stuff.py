from __future__ import unicode_literals, division, print_function
import string
from spacy.en import English
from gensim import corpora
from nltk.corpus import stopwords


class DocTokenizer(object):
    def __init__(self, filename):
        self.filename = filename
        self.nlp = English()

    def __iter__(self):
        with open(self.filename) as infile:
            for line in infile:
                doc = self.nlp(unicode(line.strip().lower()))
                yield [tok.orth_ for tok in doc]


class CorpusStreamer(object):
    def __init__(self, filename):
        self.dt = DocTokenizer(filename)
        self.dictionary = corpora.Dictionary(self.dt)
        self.stopwords = (stopwords.words('english') +
                          list(string.punctuation) +
                          list(string.whitespace))
        stop_ids = [self.dictionary.token2id[stopword] for stopword
                    in self.stopwords if stopword in self.dictionary.token2id]
        once_ids = [tokenid for tokenid, docfreq
                    in self.dictionary.dfs.iteritems() if docfreq == 1]
        self.dictionary.filter_tokens(stop_ids + once_ids)
        self.dictionary.compactify()
        print(self.dictionary)

    def save_dict(self, filename):
        self.dictionary.save(filename)

    def save_mm(self, filename):
        corpora.MmCorpus.serialize(filename, self)

    def __iter__(self):
        for doc in self.dt:
            yield self.dictionary.doc2bow(doc)
