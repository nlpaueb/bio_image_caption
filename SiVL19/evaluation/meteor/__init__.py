import re
from meteor import Meteor
import sys
import pandas as pd

scorer = Meteor()
bioclean = lambda t: re.sub('[.,?;*!%^&_+():-\[\]{}]', '', t.replace('"', '').replace('/', '').replace('\\', '').replace("'",'').strip().lower())

def main(filepath):
	gts = {}
	res = {}

	results = pd.read_json(filepath, orient="records", lines=True)
	results.predicted_caption.apply(bioclean)
	results.true_caption.apply(bioclean)

	for _, r in results.iterrows():
		gts[r.id] = [r.true_caption]
		res[r.id] = [r.predicted_caption]

	score, scores = scorer.compute_score(gts, res)

	print(score)

if __name__ == "__main__":
	main(sys.argv[1])