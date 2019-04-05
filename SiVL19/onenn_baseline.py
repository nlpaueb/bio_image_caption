import sys
sys.path.append("..")  # Adds higher directory to python modules path.
from img2vec.img_to_vec import Img2Vec
from PIL import Image
import torch.nn as nn
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from PIL import Image
from tqdm import tqdm
import pickle
import numpy as np
import os

def most_similar(filepath, images_path):
	img2vec = Img2Vec(cuda=True)

	train_path = os.path.join(filepath, "train_images.tsv")
	test_path = os.path.join(filepath, "test_images.tsv")
	results_path = os.path.join(filepath, "onenn_results.tsv")

	#load train data
	train_data = pd.read_csv(train_path, sep="\t", header=None) 
	train_data.columns = ["id", "caption"]
	train_images = dict(zip(train_data.id, train_data.caption))
	
	print("Calculating visual embeddings from train images")
	train_images_vec = {}
	print("Extracting embeddings for all train images...")
	for train_image in tqdm(train_data.id):
		image = Image.open(os.path.join(images_path, train_image))
		image = image.convert('RGB')
		vec = img2vec.get_vec(image)
		train_images_vec[train_image] = vec
	print("Got embeddings for train images.")

	#get embeddings of test images
	test_data = pd.read_csv(test_path, sep="\t", header=None)
	test_data.columns = ["id", "caption"]

	# save IDs and raw image vectors seperately but aligned
	ids = [i for i in train_images_vec]
	raw = np.array([train_images_vec[i] for i in train_images_vec])

	# normalize image vectors to avoid normalizated cosine and use dot
	raw = raw / np.array([np.sum(raw,1)] * raw.shape[1]).transpose()
	sim_test_results = {}
	for test_image in tqdm(test_data.id):
		image = Image.open(os.path.join(images_path, test_image))
		image = image.convert('RGB')
		vec = img2vec.get_vec(image)
		vec = vec / np.sum(vec)
		# clone to do efficient mat mul dot
		test_mat = np.array([vec] * raw.shape[0])
		sims = np.sum(test_mat * raw, 1)
		#denom = np.sqrt(np.sum(test_mat*test_mat,1)) * np.sqrt(np.sum(raw*raw,1))
		#sims = dots * np.array([1/denom] * test_mat.shape[1])
		top1 = np.argmax(sims)
		sim_test_results[test_image] = train_images[ids[top1]]

	#save to results dictionary the test image and the caption of the train image with max similarity
	pd.DataFrame(sim_test_results.items()).to_csv(results_path, sep="\t", header=None, index=None)