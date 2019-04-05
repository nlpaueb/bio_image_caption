 
# Datasets

First, to obtain the Peir Gross and IU X-ray datasets run the get_iu_xray.py and get_peir_gross.py. The datasets will be downloaded in the corresponding folder 
and split to train and test sets in the form of tsv files.
To obtain the ImageCLEF dataset follow the instructions described here, in the Participant registration section. 
After downloading the dataset you can run the imageCLEF_dataset.py to split the provided training data to train and test.

# Baselines

main.py performs the preprocessing, runs the frequency and the 1NN baselines and computes the wmd.
Also the json files of the results and the test sets are created in the desired mscoco format to be later used for the mscoco evaluation.

Before running the main.py git clone the Image 2 vec project (https://github.com/christiansafka/img2vec ) out of the sivl_code folder, to use for the image embedding extraction. 
You also need to download the pretrained embeddings and unzip them in the sivl_code folder running the following commands:
- wget https://archive.org/download/pubmed2018_w2v_200D.tar/pubmed2018_w2v_200D.tar.gz
- tar xvzf pubmed2018_w2v_200D.tar.gz

When main script finishes the resulted tsv and json files will be in each dataset folder.

# Εvaluation

The mscoco evaluation code was used and is in the coco_caption folder. To run the code you need to create a new environment with the following requirements:
- java 1.8.0
- python 2.7

You will first need to download the Stanford CoreNLP 3.6.0 (http://stanfordnlp.github.io/CoreNLP/index.html ) code and models for use by SPICE. 
To do this, in the coco_caption folder run: ./get_stanford_models.sh

Then, to perform the evaluation run the mscoco_eval.py, found in the sivl_code folder.
