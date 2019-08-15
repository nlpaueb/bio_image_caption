import re
from meteor import Meteor
import sys
import pandas as pd
import tensorflow as tf

scorer = Meteor()
# clean for BioASQ https://github.com/nlpaueb/aueb-bioasq6
bioclean = lambda t: re.sub('[.,?;*!%^&_+():-\[\]{}]', '', t.replace('"', '').replace('/', '').replace('\\', '').replace("'",'').strip().lower())

FLAGS = tf.app.flags.FLAGS

tf.flags.DEFINE_string("filepath", "", "Path to JSON file")

def main(argv):
	"""
	run as:
	>> python __init__.py --filepath "path_to_json"
	:param filepath: path to json file (json format: [{"id":"", "predicted_caption":"", "true_caption":""}]
	:return: print METEOR score
	"""

	assert FLAGS.filepath, "--filepath is required"

	gts = {}
	res = {}

	results = pd.read_json(FLAGS.filepath, orient="records")
	results.predicted_caption = results.predicted_caption.apply(bioclean)
	results.true_caption = results.true_caption.apply(bioclean)

	gts = dict(zip(results.id, results.true_caption))
	res = dict(zip(results.id, results.predicted_caption))

	gts = {k: [v] for k, v in gts.items()}
	res = {k: [v] for k, v in res.items()}

	score, scores = scorer.compute_score(gts, res)

	print("Meteor score is %s" % score)
	return score

if __name__ == "__main__":
	tf.app.run()