import gensim
import re
import argparse
import pandas as pd


# Word Mover's Distance computes the minimum cumulative cost required to move all word embeddings of one caption
# to aligned word embeddings of the other caption. We used Gensim's implementation of WMD (https://goo.gl/epzecP)
# and biomedical word2vec embeddings (https://archive.org/details/pubmed2018_w2v_200D.tar).
# WMD scores are also expressed as similarity values: WMS = (1 + WMD)^-1


parser = argparse.ArgumentParser(description="Takes as arguments a file with the gold captions, "
                                             "a file with the generated ones and a file with pre-trained embeddings "
                                             "and computes WMD and WMS scores")
parser.add_argument("gold", help="Path to tsv file with gold captions")
parser.add_argument("generated", help="Path to tsv file with generated captions")
parser.add_argument("embeddings", help="Path to bin file with of pre-trained embeddings")


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
        pr_captions[image] = bioclean(images_captions[image])

    return pr_captions


def compute_wmd(gts, res, bio_path):
    """

    :param gts: Dictionary with the image ids and their gold captions
    :param res: Dictionary with the image ids ant their generated captions
    :param bio_path: Path to the pre-trained biomedical word embeddings
    :print: WMD and WMS scores
    """

    # Preprocess captions
    gts = preprocess_captions(gts)
    res = preprocess_captions(res)

    # Load word embeddings
    bio = gensim.models.KeyedVectors.load_word2vec_format(bio_path, binary=True)
    print("Loaded word embeddings")

    # Calculate WMD for each gts-res captions pair
    print("Calculating wmd for each pair...")
    total_distance = 0
    img_wmds, similarities = {}, {}

    assert len(gts) == len(res)

    for image in gts:
        distance = bio.wmdistance(gts[image].split(), res[image].split())
        similarities[image] = (1. / (1. + distance))
        total_distance = total_distance + distance
        img_wmds[image] = distance

    # calculate mean wmd
    wmd = total_distance / float(len(gts))
    wms = sum(similarities.values()) / float(len(similarities))

    print("WMD =", wmd, ", WMS =", wms)


if __name__ == "__main__":

    args = parser.parse_args()
    gold_path = args.gold
    results_path = args.generated
    bio_embeddings_path = args.embeddings

    # Load data
    gts_data = pd.read_csv(gold_path, sep="\t", header=None, names=["image_ids", "captions"])
    gts = dict(zip(gts_data.image_ids, gts_data.captions))

    res_data = pd.read_csv(results_path, sep="\t", header=None, names=["image_ids", "captions"])
    res = dict(zip(res_data.image_ids, res_data.captions))

    # Compute evaluation scores
    compute_wmd(gts, res, bio_embeddings_path)
