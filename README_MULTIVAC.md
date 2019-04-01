# Query Generation Network (QG-Net)
## Acknowledgements
[QG-Net](https://github.com/moonlightlane/QG-Net) was developed by Z. Wang,
A. S. Lan, W. Nie, P. Grimaldi, A. E. Waters, and R. G. Baraniuk and appeared
as a key part of their work presented at ACM Conference on Learning at Scale
(L@S) in June 2018. The publication citation:

Z. Wang, A. S. Lan, W. Nie, P. Grimaldi, A. E. Waters, and R. G. Baraniuk. QG-Net: A Data-Driven Question Generation Model for Educational Content. ACM Conference on Learning at Scale (L@S), June 2018, Article 7, pp. 1-10, doi: 10.1145/3231644.3231654.

Full text of their publication is available [here](https://people.umass.edu/~andrewlan/papers/18l@s-qgen.pdf).

## Introduction
For its [MULTIVAC](https://github.com/GallupGovt/multivac) effort on behalf of
the Defense Advanced Research Projects Agency (DARPA), Gallup has modified and
used query generation networks (QG-Net) as adapted from Wang et. al., cited
above. The text below focuses specifically on the QG-Net portion of the
MULTIVAC effort. For more in general on MULTIVAC, please visit the primary
[repository](https://github.com/GallupGovt/multivac) README.

## Query Training
MULTIVAC derives queries from text using a modified version of the deep
learning query generation system (QG-Net). QG-Net is a recurrent neural network
(RNN)-based model that takes as inputs a "context" (typically a limited amount
of natural language text containing relevant information) and an "answer" (a
specific fact or figure found within the context) and outputs a question
tailored to produce that answer. For MULTIVAC, we provided epidemiology
research abstracts to the QG-Net context reader. The abstract is the section
most authors use to communicate the research succinctly while highlighting its
most important facets. MULTIVAC uses the five most important sentences in the
abstract as the "context" and uses the most important words/phrases in each of
the five sentences of the abstract as the “answer.” Term frequency-inverse
document frequency (TF-IDF) scores are calculated to determine which terms/
sentences in the documents are truly important and differentiating. The five
sentences with the largest total sum of their terms' TF-IDF scores are used to
generate queries. Within the top five sentences, the term or consecutive terms
with the highest TF-IDF scores are tagged as "answers."

![alt text](https://github.com/GallupGovt/multivac/blob/master/images/qgnet.png 'QG-net schematic')
<br>Illustration of the QG-Net system. Source: https://github.com/moonlightlane/QG-Net

Given context and answer inputs, QG-Net generates different questions that
focus on the relevant contextual information that different answers provide.
More specifically, QG-Net uses [GloVe](https://nlp.stanford.edu/projects/glove/),
an unsupervised learning algorithm for modeling word embeddings, to represent
words as vectors coupled with speech tag (POS), name entity recognition (NER),
and word case (CAS) from the Stanford natural language processing toolkit as
inputs in the context reader. In addition, the QG-Net input includes a
binary-valued indicator to indicate whether a word is the "answer." Finally,
the question generator generates diverse question text word-by-word given all
context word representations.

## Query Output
The resulting queries are then applied in order to MULTIVAC’s Markov logic
network (MLN) ontology and the resulting answers are compared with the "answer"
extracted directly from the source data. Good matches, in the sense of high
scores for semantic completeness, lexical similarity, and syntactical
similarity will indicate good performance. These measures will be assessed
using approaches including but not necessarily limited to latent semantic
analysis and minimal edit distance metrics. With QG-Net, we generated 2,804
queries based on epidemiology research abstracts scraped and processed as
earlier steps in MULTIVAC.

## Dependencies
To run QG-Net, there are a number of dependencies above and beyond those required for MULTIVAC. Primary among them is the need for a GPU-based system (currently tested against a Nvidia Quadro Pro-4000 card) for computation of the RNN. In addition to the GPU, the following are core requirements:
- GPU for computation
- Python 3.6
- pytorch-0.4.1
- OpenNMT-py (note, the version of OpenNMT-py in the original QG-Net is necessary for execution; not tested with MIT's version of OpenNMT)
- [Stanford CoreNLP server](https://stanfordnlp.github.io/CoreNLP/#download)
- torchtext-0.1.1
- [DrQA] (https://github.com/facebookresearch/DrQA)

## Directions to run QG-Net as a stand-alone application for MULTIVAC
1.  Clone the [QG-Net repository on GallupGovt](https://github.com/GallupGovt/qgnet) to implement QG-Net within the MULTIVAC system.
2.  The MULTIVAC instantiation of QG-Net uses a domain-adapted GloVe model. This should be a text file outputted from an earlier step of the MULTIVAC system. It needs to be updated, within the QG-Net repo, in the following file: `./OpenNMT-py/opts.py`.
3.  Run the download script `download_QG-Net.sh` in the top-level directory in a terminal window to download a pre-trained QG-Net model. You may need to modify the shell script to fit your needs. This will create the QG-Net model needed for modeling.
4. The Python script `preprocessing_pdf.py` in the `./test/` folder takes the epidemiological research articles as inputs in the form of JSON files. Using the JSON files, the Python script generates the `input.txt` file which includes the "context" and "answers" needed for input into the QG-Net system. The `input.txt` file is saved in the `./test/input.for.test/` directory.
4.  Run the script in the `./test/` folder; first `cd test/`, then run the shell script `qg_reproduce_LS.sh`. This takes the file `input.txt` and generates questions using the QG-Net algorithm. The final output is saved in the `./test/` folder and called `output_questions_QG-Net.pt.txt`.
