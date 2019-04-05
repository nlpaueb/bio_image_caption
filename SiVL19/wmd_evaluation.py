import gensim
import re
import os

def load_tsv(filename):
	images = {}

	with open(filename, "r") as file:
		for line in file:
			line = line.replace("\n", "").split("\t")
			images[line[0]] = line[1]

	return images

def preprocess_data(pairs):

	# clean for BioASQ
	bioclean = lambda t: re.sub('[.,?;*!%^&_+():-\[\]{}]', '', t.replace('"', '').replace('/', '').replace('\\', '').replace("'",'').strip().lower()).split()

	pr_pairs = {}
	for pair in pairs:
		tokens = bioclean(pairs[pair])
		pr_pairs[pair] = " ".join(tokens)

	return pr_pairs


def compute_wmd(gts, res, bio_path):

	bio = gensim.models.KeyedVectors.load_word2vec_format(bio_path, binary=True)
	print("Loaded word embeddings")

	#calculate wmd for each gts-res captions pair
	print("Calculating wmd for each pair...")
	total_distance = 0
	img_wmds,similarities = {},{}

	assert len(gts) == len(res)

	for image in gts:
		distance = bio.wmdistance(gts[image].split(), res[image].split())
		similarities[image] = (1./(1.+distance))
		total_distance = total_distance + distance
		img_wmds[image] = distance

	#calculate mean wmd
	wmd = total_distance / float(len(gts))
	wms = sum(similarities.values())/float(len(similarities))

	return wmd, wms


def evaluate(filepath, bio_path):

	gts = load_tsv(os.path.join(filepath, "test_images.tsv"))
	freq_results = load_tsv(os.path.join(filepath, "freq_results.tsv"))
	onenn_results = load_tsv(os.path.join(filepath, "onenn_results.tsv"))

	pr_gts = preprocess_data(gts)
	pr_onenn_results = preprocess_data(onenn_results)

	#evaluate frequency results
	freq_wmd, freq_wms = compute_wmd(pr_gts, freq_results, bio_path)
	print("For frequency baseline: wmd =", freq_wmd, ", wms =", freq_wms)

	#evaluate onenn results
	onenn_wmd, onenn_wms = compute_wmd(pr_gts, pr_onenn_results, bio_path)
	print("For 1NN baseline: wmd =", onenn_wmd, ", wms =", onenn_wms)