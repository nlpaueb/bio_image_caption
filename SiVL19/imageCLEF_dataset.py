import random
import os
import numpy
from shutil import rmtree

def split_images(images, keys, filename):
	new_images = {}

	for key in keys:
		new_images[key] = images[key]

	with open(filename, "w") as output_file:
		for new_image in new_images:
			output_file.write(new_image + "\t" + new_images[new_image])
			output_file.write("\n")

# create dataset folder
try:
	rmtree("imageCLEF/")
except BaseException:
	pass
os.makedirs("imageCLEF/")

# load data
images = {}

with open("CaptionPredictionTraining2018-Captions.csv", "r") as file:
	for line in file:
		line = line.replace("\n", "").split("\t")
		images[line[0] + ".jpg"] = line[1]

keys = list(images.keys())
keys.sort()

# split data
random.seed(42)
random.shuffle(keys)

train_split = int(numpy.floor(len(images) * 0.9))

train_keys = keys[:train_split]
test_keys = keys[train_split:]

split_images(images, train_keys, "imageCLEF/train_images.tsv")
split_images(images, test_keys, "imageCLEF/test_images.tsv")
