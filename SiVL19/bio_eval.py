import re
from pycocoevalcap.bleu.bleu import Bleu
from pycocoevalcap.meteor.meteor import Meteor
from pycocoevalcap.rouge.rouge import Rouge
# from pycocoevalcap.cider.cider import Cider
# from pycocoevalcap.spice.spice import Spice

class BioEvalCap:
	def __init__(self, coco, cocoRes):
		self.evalImgs = []
		self.eval = {}
		self.imgToEval = {}
		self.coco = coco
		self.cocoRes = cocoRes
		self.params = {'image_id': coco.getImgIds()}

	def evaluate(self, bio=False):
		imgIds = self.params['image_id']
		# imgIds = self.coco.getImgIds()
		gts = {}
		res = {}
		for imgId in imgIds:
			gts[imgId] = self.coco.imgToAnns[imgId]
			res[imgId] = self.cocoRes.imgToAnns[imgId]

		# =================================================
		# Set up scorers
		# =================================================
		print 'tokenization...'
		gts  = self.tokenize(gts)
		res = self.tokenize(res)

		# =================================================
		# Set up scorers
		# =================================================
		print 'setting up scorers...'
		scorers = [
			(Bleu(4), ["Bleu_1", "Bleu_2", "Bleu_3", "Bleu_4"]),
			(Meteor(),"METEOR"),
			(Rouge(), "ROUGE_L"),
			# (Cider(), "CIDEr"),
			# (Spice(), "SPICE")
		]

		# =================================================
		# Compute scores
		# =================================================
		for scorer, method in scorers:
			print 'computing %s score...'%(scorer.method())
			score, scores = scorer.compute_score(gts, res)
			if type(method) == list:
				for sc, scs, m in zip(score, scores, method):
					self.setEval(sc, m)
					self.setImgToEvalImgs(scs, gts.keys(), m)
					print "%s: %0.3f"%(m, sc)
			else:
				self.setEval(score, method)
				self.setImgToEvalImgs(scores, gts.keys(), method)
				print "%s: %0.3f"%(method, score)
		self.setEvalImgs()


	def setEval(self, score, method):
		self.eval[method] = score

	def setImgToEvalImgs(self, scores, imgIds, method):
		for imgId, score in zip(imgIds, scores):
			if not imgId in self.imgToEval:
				self.imgToEval[imgId] = {}
				self.imgToEval[imgId]["image_id"] = imgId
			self.imgToEval[imgId][method] = score

	def setEvalImgs(self):
		self.evalImgs = [eval for imgId, eval in self.imgToEval.items()]

	def tokenize(self, captions):

		# clean for BioASQ
		bioclean = lambda t: re.sub('[.,?;*!%^&_+():-\[\]{}]', '', t.replace('"', '').replace('/', '').replace('\\', '').replace("'",'').strip().lower()).split()
		tokenized_captions = {}

		for image in captions:
			new_caption = []
			tokens = bioclean(captions[image][0]["caption"])

			new_caption.append(" ".join(tokens).encode("utf-8"))
			tokenized_captions[image] = new_caption

		return tokenized_captions
