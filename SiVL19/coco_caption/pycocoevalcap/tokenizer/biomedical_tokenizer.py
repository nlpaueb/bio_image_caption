import re

class BIOtokenizer:

	def tokenize(self, captions):

		# clean for BioASQ
		bioclean = lambda t: re.sub('[.,?;*!%^&_+():-\[\]{}]', '', t.replace('"', '').replace('/', '').replace('\\', '').replace("'",'').strip().lower()).split()
		tokenized_captions = {}

		for image in captions:
			new_caption = []
			tokens = bioclean(captions[image][0]["caption"])

			new_caption.append(" ".join(tokens))
			tokenized_captions[image] = new_caption

	        return tokenized_captions
