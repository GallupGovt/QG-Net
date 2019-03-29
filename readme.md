## Query Training
### Confirm Execution of Queries as Models
MULTIVAC will accept properly formatted queries, parse them into compatible formats and match their components to relevant nodes and clusters in its MLN knowledge base to produce answers for those queries. This functionality will be tested and refined in several ways, first using queries auto-extracted from the source texts and then with human expert review. 

MULTIVAC will extract literal expert queries, identified by parsing full texts into component sentences and selecting sentences that end in question marks, as well as deriving expert queries from abstracts using a modified version of deep learning query-generation system QG-Net.<sup>[1](#1)</sup>  QG-Net is a recurrent neural network (RNN)-based model that takes as inputs a “context” (typically a limited amount of natural language text containing relevant information) and an “answer” (a specific fact or figure found within the context) and outputs a question tailored to produce that answer. Our adaptation of QG-Net will be written in Python, in line with the current implementation and the rest of the MULTIVAC system.

MULTIVAC supplies article abstracts from the metadata file saved from the initial datastore acquisition. These abstracts serve as the “context” data, and MULTIVAC will select parts of the abstracts as the “answer” data. These parts will be selected based on two heuristics:
* Words that occur in the same context (sentence or paragraph) as model parameters and descriptions in the main body of the article or that occur in the article title signify phrases that can serve as feasible answers.
* Words with a high TF-IDF score for a particular article signify phrases that can serve as feasible answers.

![alt text](https://github.com/GallupGovt/multivac/blob/master/images/qgnet.png 'QG-net schematic')
<br>Illustration of the QG-net system. Source: https://github.com/moonlightlane/QG-Net

Given context and answer inputs, QG-Net generates different questions that focus on the relevant contextual information that different answers provide. More specifically, it uses MULTIVAC’s domain-adapted GloVe embedding model to represent words as vectors coupled with speech tags, name entity flags and word case tags from the initial parsing as inputs in the context reader to generate diverse context word representations. Finally, a question generator generates the question text word-by-word given all context word representations.

The resulting queries are then applied in order to MULTIVAC’s MLN ontology and the resulting answers are compared with the “answer” extracted directly from the source data. Good matches, in the sense of high scores for semantic completeness, lexical similarity and syntactical similarity will indicate good performance of the ontology. These measures will be assessed using approaches including but not necessarily limited to latent semantic analysis and minimal edit distance metrics. 

This process serves an important quality control purpose, but more importantly this round of query generation allows MULTIVAC to bootstrap a training data set for learning how to generate its own queries without direct reference to previously existing research questions or findings. Samples of this training data will be reviewed and vetted by live human experts as a template for the essential inclusion of human expertise in MULTIVAC’s workflow in eventual production versions of the system. These human experts will also test the trained system with their own novel queries. The involvement of human experts in this phase serves two purposes. First, human expert review of the extracted queries and outputs provides a crucial check on system performance and helps identify areas most in need of improvement or optimization. Second, novel queries submitted by actual human experts provides an “out of sample” test for a system trained on a finite corpus.

### Dependencies
python3.5 \
pytorch (only tested on v0.4.1) \
GPU for computation \
OpenNMT-py (not tested on the latest version; pls use the version in this repo) \
Stanford CoreNLP download and server \
torchtext-0.1.1 (this is important; if you use the latest 
torchtext you might encounter error when preprocessing 
corpus. Install by the command `pip3 install torchtext-
0.1.1`, or follow official installation instructions for
your python distribution.)

### Directions to run QG-Net algorithm to generate queries. 
1. Run the download script to download a pre-trained QG-Net model
and the test input file: `. download_QG-Net.sh`
2. Run the script in the `test` folder; first `cd test/`, then
`. qg_reproduce_LS.sh`
3. The output file is a text file starting with 
 the prefix `output_questions_`

### End Notes
- <sup><a name='1'>1</a></sup> Z. Wang, A. S. Lan, W. Nie, P. Grimaldi, R. Schloss, and R. G. Baraniuk, "QG-Net: A Data-Driven Question Generation Model for Educational Content," ACM Conference on Learning at Scale (L@S), pp. 1-10, June 2018. Full text available at https://people.umass.edu/~andrewlan/papers/18l@s-qgen.pdf <br>

