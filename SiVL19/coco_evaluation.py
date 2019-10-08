import re
import argparse
import pandas as pd
from pycocoevalcap.bleu.bleu import Bleu
from pycocoevalcap.meteor.meteor import Meteor
from pycocoevalcap.rouge.rouge import Rouge

parser = argparse.ArgumentParser(description="Takes as arguments a file with the gold captions and "
                                             "a file with the generated ones and computes "
                                             "BLEU 1-4, METEOR and Rouge-L measures")
parser.add_argument("gold", help="Path to tsv file with gold captions")
parser.add_argument("generated", help="Path to tsv file with generated captions")


def preprocess_captions(images_captions):
    """

    :param images_captions: Dictionary with image ids as keys and captions as values
    :return: Dictionary with the processed captions as values
    """

    # Clean for BioASQ
    bioclean = lambda t: re.sub('[.,?;*!%^&_+():-\[\]{}]', '',
                                t.replace('"', '').replace('/', '').replace('\\', '').replace("'",
                                                                                              '').strip().lower())
    pr_captions = {}
    # Apply bio clean to data
    for image in images_captions:
        # Save caption to an array to match MSCOCO format
        pr_captions[image] = [bioclean(images_captions[image])]

    return pr_captions


def compute_scores(gts, res):
    """
    Performs the MS COCO evaluation using the Python 3 implementation (https://github.com/salaniz/pycocoevalcap)

    :param gts: Dictionary with the image ids and their gold captions,
    :param res: Dictionary with the image ids ant their generated captions
    :print: Evaluation score (the mean of the scores of all the instances) for each measure
    """

    # Preprocess captions
    gts = preprocess_captions(gts)
    res = preprocess_captions(res)

    # Set up scorers
    scorers = [
        (Bleu(4), ["Bleu_1", "Bleu_2", "Bleu_3", "Bleu_4"]),
        (Meteor(), "METEOR"),
        (Rouge(), "ROUGE_L")
    ]

    # Compute score for each metric
    for scorer, method in scorers:
        print("Computing", scorer.method(), "...")
        score, scores = scorer.compute_score(gts, res)
        if type(method) == list:
            for sc, m in zip(score, method):
                print("%s : %0.3f" % (m, sc))
        else:
            print("%s : %0.3f" % (method, score))


if __name__ == "__main__":

    args = parser.parse_args()
    gold_path = args.gold
    results_path = args.generated

    # Load data
    gts_data = pd.read_csv(gold_path, sep="\t", header=None, names=["image_ids", "captions"])
    gts = dict(zip(gts_data.image_ids, gts_data.captions))

    res_data = pd.read_csv(results_path, sep="\t", header=None, names=["image_ids", "captions"])
    res = dict(zip(res_data.image_ids, res_data.captions))

    compute_scores(gts, res)