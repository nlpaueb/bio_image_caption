A Survey on Biomedical Image Captioning
=================

Implementation of the baseline and evaluation methods described in the [paper.](https://arxiv.org/abs/1905.13302)

## Datasets ##

We provide scripts for downloading IU X-ray and Peir Gross datasets. The ImageCLEF2018 dataset is not publicly 
available, so to download it you need to follow the instructions described [here](https://www.imageclef.org/2018/caption), 
in the Participant registration section. Then, you can run the corresponding script that uses the downloaded *csv*
file.
For each dataset a folder is created that contains the images and the data *tsv* files with 
the following format: *image_name <\t> caption*.


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

The evaluation with the WMS can be performed as shown in *sivl_run_me.ipynb*.
To evaluate with the BLEU 1-4, METEOR and ROUGE measures we used the [MS COCO caption evaluation code](https://github.com/tylin/coco-caption).
After you git clone the code and have the specified requirements run the following commands to move our 
two scripts in the coco-caption folder and perform the evaluation. 
To run the main script *mscoco_main_eval.py* give as arguments the path to the dataset folder that contains 
the *json* files and the dataset name.
```shell
git clone https://github.com/tylin/coco-caption.git
mv bio_image_caption/SiVL19/mscoco_main_eval.py coco-caption/
mv bio_image_caption/SiVL19/bio_eval.py coco-caption/
python coco-caption/mscoco_main_eval.py /dataset_folder dataset_name
```

