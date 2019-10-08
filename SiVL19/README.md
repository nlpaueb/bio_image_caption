A Survey on Biomedical Image Captioning
=================

Code to download and preprocess the datasets, run the baselines and evaluate 
the results as described in the paper 
[A Survey on Biomedical Image Captioning](https://www.aclweb.org/anthology/W19-1803).

> V. Kougia, J. Pavlopoulos and I Androutsopoulos, "A Survey on Biomedical Image Captioning". 
Proceedings of the Workshop on Shortcomings in Vision and Language of the Annual Conference 
of the North American Chapter of the Association for Computational Linguistics (NAACL-HLT 2019), Minneapolis, USA, 2019.

## Dependencies ##
To use this code you will need to install python 3.6 and the packages from the requirements.txt file. To install them run 
```shell
pip install -r requirements.txt.
```
To use the MS COCO evaluation script (coco_evaluation.py) follow the instructions described [here](https://github.com/salaniz/pycocoevalcap) to install the library.

## Datasets ##

We provide scripts for downloading IU X-ray and Peir Gross datasets. The ImageCLEF2018 dataset is not publicly 
available, so to download it you need to follow the instructions described [here](https://www.imageclef.org/2018/caption), 
in the Participant registration section. Then, you can run the corresponding script that uses the downloaded *csv*
file.
For each dataset a folder is created that contains the images and the data *tsv* files with 
the following format: *image_name <\t> caption*. All data files as well as the results files should follow this format.


```shell
cd bio_image_caption/SiVL19
# IU X-ray:
python get_iu_xray.py
# Peir Gross:
python get_peir_gross.py
# ImageCLEF2018:
python imageCLEF_dataset.py
```

## Baselines ##

For the instructions on how to perform the preprocessing and run the baselines for a given dataset see 
the demo script *sivl_run_me.ipynb*.

## Evaluation ##

The evaluation with the WMD and the MS COCO captioning measures can be performed as in *sivl_run_me.ipynb*.
You can either use the *compute_wmd* and *compute_scores* methods for the WMD and MS COCO evaluations respectively (as shown in *sivl_run_me.ipynb*) 
or run the main methods of the scripts providing the necessary arguments as shown below:
```shell
# For the WMD evaluation:
python wmd_evaluation.py path_to_gold_captions/gold.tsv path_to_results/results.tsv path_to_embeddings/emb.bin

# For the MSCOCO evalaution:
python coco_evaluation.py path_to_gold_captions/gold.tsv path_to_results/results.tsv
```
