#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pickle
import warnings

from sklearn.feature_extraction.text import TfidfVectorizer
from sortedcontainers import SortedDict

from multivac import settings


def create_tf_idf(docs, writeFile=True, pathToFolders=''):
    """ Creates a TF-IDF matrix of terms in the corpus and saves this to disk
        as a sparse matrix in the data/processed folder when writeFile=True and
        pathToFolders is provided.
    """
    tfidf = TfidfVectorizer(sublinear_tf=True,
                            min_df=10,
                            norm=None,
                            ngram_range=(1, 3),
                            stop_words='english',
                            use_idf=True,
                            smooth_idf=True)

    features = tfidf.fit_transform(docs)

    if writeFile:
        if len(pathToFolders) == 0:
            pathToFolders = settings.processed_dir

        with open(pathToFolders / 'multivac_tfidf.pkl', 'wb') as f:
            pickle.dump({'features': features, 'tfidf': tfidf}, f)

        return True
    else:
        return features, tfidf


def preprocess_pdf(abstract, features, tfidf, nlp, num_sentences=5):
    '''
    Chooses top `num_sentences` based on the sum of their terms' TF-IDF scores,
    and then picks the word/term in each sentence with the top TF-IDF score as
    the "answer."
    '''
    document = nlp.annotate(abstract)
    term_scores = [(w,s) for w, s in zip(tfidf.get_feature_names(),
                                         features.reshape(-1)) if s > 0]
    sent_scores = SortedDict()

    for i, sentence in enumerate(document['sentences']):
        score = sum([s for w, s in term_scores if w in str(sentence)])
        sent_scores[score] = i

    warnings.filterwarnings('ignore', category=UserWarning, append=True)

    output_vec = []
    for i in reversed(sent_scores.values()):
        out_str = ''
        if i >= num_sentences:
            break

        sentence = document['sentences'][i]
        str_sent = ' '.join([t['originalText'] for t in sentence['tokens']])
        top_term = sorted([(w,s) for w, s in term_scores if w in str_sent],
                             key=lambda x: x[1], reverse=True)[0][0]
        top_term = top_term.split()

        for i, token in enumerate(sentence['tokens']):
            tok_text = token['originalText']

            if tok_text[0].isupper():
                low = 'U'
            else:
                low = 'L'

            if len(top_term) > 0:
                ans = 'A'
            else:
                ans = '-'

            for j, t in enumerate(top_term):
                if sentence['tokens'][i+j]['originalText'] != top_term[j]:
                    ans = '-'
                    break

            if ans =='A' and len(top_term) > 0:
                del top_term[0]

            out_str += "{}￨{}￨{}￨{}￨{} ".format(tok_text, low, token['pos'],
                                                   token['ner'], ans)

        if '￨A' in out_str:
            output_vec.append(out_str[:-1])

    with open('{}/test/testinput/input.txt'.format(settings.qgnet_dir),
              'w') as f:
        f.write('\n'.join(output_vec))

    return None
