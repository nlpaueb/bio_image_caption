import re
import os


def create_vocabulary(filepath):

	# clean for BioASQ
	bioclean = lambda t: re.sub('[.,?;*!%^&_+():-\[\]{}]', '', t.replace('"', '').replace('/', '').replace('\\', '').replace("'",'').strip().lower()).split()

	total_words = []
	pr_captions = []

	#load data
	train_path = os.path.join(filepath, "train_images.tsv")

	with open(train_path, "r") as file:

		for line in file:
			line = line.replace("\n", "").split("\t")

			tokens = bioclean(line[1])
			for token in tokens:
				total_words.append(token)
			caption = " ".join(tokens)
			pr_captions.append(caption)


	print("Total number of captions is",len(pr_captions))

	unique_captions = set(pr_captions)
	print("Total number of unique captions is", len(unique_captions))

	mean_length = len(total_words)/len(pr_captions)
	print("The average caption length is", mean_length, "words")

	#create vocabulary of unique words
	vocabulary = set(total_words)
	print("Unique words are", len(vocabulary))
	with open(os.path.join(filepath, "vocabulary.txt"), 'w') as output_file:
		for word in vocabulary:
			output_file.write(word)
			output_file.write("\n")
    

	return mean_length
