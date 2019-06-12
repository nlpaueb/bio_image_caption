 
from pycocotools.coco import COCO
from bio_eval import BioEvalCap

import sys
import os
import json
from json import encoder
encoder.FLOAT_REPR = lambda o: format(o, '.3f')


def coco_evaluate(filepath, results_path):

	annFile = os.path.join(filepath, "test_images.json")
	freq_resFile = os.path.join(filepath, "freq_results.json")
	onenn_resFile = os.path.join(filepath, "onenn_results.json")

	# create coco object
	coco = COCO(annFile)

	# create cocoRes objects for frequency and onenn baselines evaluation
	freq_cocoRes = coco.loadRes(freq_resFile)
	onenn_cocoRes = coco.loadRes(onenn_resFile)

	# create two cocoEval objects by taking coco and cocoRes objects
	freq_cocoEval = BioEvalCap(coco, freq_cocoRes)
	onenn_cocoEval = BioEvalCap(coco, onenn_cocoRes)

	# evaluate frequency results
	print "Frequency baseline evaluation:"
	freq_cocoEval.evaluate(True)

	# print output evaluation scores
	for metric, score in freq_cocoEval.eval.items():
		print '%s: %.3f'%(metric, score)

	# evaluate onenn results
	print "1NN baseline evaluation:"
	onenn_cocoEval.evaluate(True)

	# print output evaluation scores
	for metric, score in onenn_cocoEval.eval.items():
		print '%s: %.3f'%(metric, score)


	# save evaluation results
	json.dump(freq_cocoEval.evalImgs, open(results_path + "_freq_evalImgs.json", 'w'))
	json.dump(freq_cocoEval.eval,     open(results_path + "_freq_eval.json", 'w'))

	json.dump(onenn_cocoEval.evalImgs, open(results_path + "_onenn_evalImgs.json", 'w'))
	json.dump(onenn_cocoEval.eval,     open(results_path + "_onenn_eval.json", 'w'))



def main(path, dataset_name):

	# set up file names and paths

	results_path = "./results/"

	print "MS Coco evaluation:"
	coco_evaluate(path, results_path + dataset_name)


if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2])
