import re
import os
from collections import Counter

def most_frequent(filepath, length):

	train_path = os.path.join(filepath, "train_images.tsv")
	test_path = os.path.join(filepath, "test_images.tsv")
	results_path = os.path.join(filepath, "freq_results.tsv")

	# clean for BioASQ
	bioclean = lambda t: re.sub('[.,?;*!%^&_+():-\[\]{}]', '', t.replace('"', '').replace('/', '').replace('\\', '').replace("'",'').strip().lower()).split()

	#load train data to find most frequent words
	words = []
	with open(train_path, "r") as file:
		for line in file:
			line = line.replace("\n", "").split("\t")
			tokens = bioclean(line[1])
			for token in tokens:
				words.append(token)


	print("The number of total words is:", len(words))

	frequent_words = Counter(words).most_common(int(round(length)))

	caption = " ".join(f[0] for f in frequent_words)

	print("The caption of most frequent words is:", caption)

	#load test images to create results
	test_images = []
	with open(test_path, "r") as file:
		for line in file:
			line = line.replace("\n", "").split("\t")
			test_images.append(line[0])

	with open(results_path, 'w') as output_file:
		for test_image in test_images:
			output_file.write(test_image + "\t" + caption)
			output_file.write("\n")