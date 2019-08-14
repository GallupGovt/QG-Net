#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 15:27:25 2019

@author: domonique_hodge
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 17:31:50 2019

@author: domonique_hodge
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  2 11:21:36 2019
@author: domonique_hodge
"""

"""
This code preprocess pdfs for the QG-Net (Query Generation) algorithm
"""

import os
os.environ["CORENLP_HOME"] = r'Users/domonique_hodge/Downloads/stanford-corenlp-full-2018-10-05'

import corenlp
import warnings
import logging
import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sortedcontainers import SortedDict
import pickle


import logging
import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sortedcontainers import SortedDict


def preprocess_pdf(abstract, features, tfidf, num_sentences=5):
    '''
    Chooses top `num_sentences` based on the sum of their terms' TF-IDF scores,
    and then picks the word/term in each sentence with the top TF-IDF score as
    the "answer."
    '''
    document = nlp.annotate(abstract)
    term_scores = [(w,s) for w, s in zip(tfidf.get_feature_names(), features.reshape(-1)) if s > 0]
    sent_scores = SortedDict()

    for i, sentence in enumerate(document['sentences']):
        score = sum([s for w, s in term_scores if w in str(sentence)])
        sent_scores[score] = i

    warnings.filterwarnings('ignore', category=UserWarning, append=True)

    try:
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
            #updated here
                out_str += "{}￨{}￨{}￨{}￨{} ".format(tok_text,low,token['pos'],token['ner'],ans)
                
            if '￨A' in out_str:
                print(out_str)
    except:
        pass
 
    
    
    
    
def load_data(jsonPath, picklePath = None):
    """Load data - if picklePath is specified, load the pickle. Else, try json file.
    This returns the JSON file as well as a list of document texts
    """
    if picklePath is not None:
        l_docs = pickle.load(open(picklePath, "rb" ))
    else:

	## Read JSON data into the datastore variable - this comes from Peter and Domonique's effort. Don
        with open(jsonPath, 'r') as f:
            datastore = json.load(f)

        ## These were some bad files - nothing substantive in them, or they were retrieved in bad format
        for e in ['1805.10677v1', '0911.5378v1']:
            if e in datastore:
                del datastore[e]

        ## Extract texts
        l_docs = [value['text'] for key,value in list(datastore.items())[0:] if value['text'] ]

    print('# of documents: ', len(l_docs))

    return datastore, l_docs


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


# ####################
#
# Substitute this hard-coded path for a path passed during the automated
# pre-processing.
#
# ####################
keysent = pickle.load( open( "/Users/domonique_hodge/Documents/External Clients/DARPA/QG Net update/key_sentences.pickle", "rb" ) )
        
topsent = []

for k in range(0,len(keysent)):
    topsent.append(' '.join(keysent[k]))
    

nlp = corenlp.CoreNLPClient(output_format='json', properties={
    'timeout': '50000'})

# Once we've determined the proper filepath to output, we can change
# this call to write the files out to disk
features, tfidf = create_tf_idf(topsent, False)

for i, abstract in enumerate(topsent):
    preprocess_pdf(abstract, features[i,:].toarray(), tfidf)