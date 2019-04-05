 
from coco_caption.pycocotools.coco import COCO
from coco_caption.pycocoevalcap.eval import COCOEvalCap

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
	freq_cocoEval = COCOEvalCap(coco, freq_cocoRes)
	onenn_cocoEval = COCOEvalCap(coco, onenn_cocoRes)

	# evaluate frequency results
	print "Frequency baseline evaluation:"
	try:
		freq_cocoEval.evaluate(True)
	except:
		print "An error ocurred during evaluation"

	# print output evaluation scores
	for metric, score in freq_cocoEval.eval.items():
		print '%s: %.3f'%(metric, score)

	# evaluate onenn results
	print "1NN baseline evaluation:"
	try:
		onenn_cocoEval.evaluate(True)
	except:
		print "An error ocurred during evaluation"

	# print output evaluation scores
	for metric, score in onenn_cocoEval.eval.items():
		print '%s: %.3f'%(metric, score)


	# save evaluation results
	json.dump(freq_cocoEval.evalImgs, open(results_path + "freq_evalImgs.json", 'w'))
	json.dump(freq_cocoEval.eval,     open(results_path + "freq_eval.json", 'w'))

	json.dump(onenn_cocoEval.evalImgs, open(results_path + "onenn_evalImgs.json", 'w'))
	json.dump(onenn_cocoEval.eval,     open(results_path + "onenn_eval.json", 'w'))



def main():

	# set up file names and paths
	peir_gross_path = "./peir_gross/"
	iu_xray_path = "./iu_xray/"
	#image_clef_path = "./imageCLEF/"

	results_path = "./coco_caption/results/"

	print "Peir Gross evaluation:"
	coco_evaluate(peir_gross_path, os.path.join(results_path, "peir_gross_"))

	print "IU X-ray evaluation:"
	coco_evaluate(iu_xray_path, os.path.join(results_path, "iu_xray_"))

	# print "ImageCLEF evaluation:"
	# coco_evaluate(image_clef_path, os.path.join(results_path, "imageCLEF_"))

if __name__ == "__main__":
	main()