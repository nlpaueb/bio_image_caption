import sys
sys.path.append("..")  # Adds higher directory to python modules path.
from img2vec_pytorch import Img2Vec
import pandas as pd
from PIL import Image
from tqdm import tqdm
import numpy as np
import os

def most_similar(train_path, test_path, images_path, results_path, cuda=False):
    """
    Nearest Neighbor Baseline: Img2Vec library (https://github.com/christiansafka/img2vec/) is used to obtain
    image embeddings, extracted from ResNet-18. For each test image the cosine similarity with all the training images
    is computed in order to retrieve similar training images.
    The caption of the most similar retrieved image is returned as the generated caption of the test image.

    :param train_path: The path to the train data tsv file with the form: "image \t caption"
    :param test_path: The path to the test data tsv file with the form: "image \t caption"
    :param images_path: The path to the images folder
    :param results_path: The folder in which to save the results file
    :param cuda: Boolean value of whether to use cuda for image embeddings extraction. Default: False
    If a GPU is available pass True
    :return: Dictionary with the results
    """

    img2vec = Img2Vec(cuda=cuda)


    # Load train data
    train_data = pd.read_csv(train_path, sep="\t", header=None)
    train_data.columns = ["id", "caption"]
    train_images = dict(zip(train_data.id, train_data.caption))

    # Get embeddings of train images
    print("Calculating visual embeddings from train images")
    train_images_vec = {}
    print("Extracting embeddings for all train images...")
    for train_image in tqdm(train_data.id):
        image = Image.open(os.path.join(images_path, train_image))
        image = image.convert('RGB')
        vec = img2vec.get_vec(image)
        train_images_vec[train_image] = vec
    print("Got embeddings for train images.")

    # Load test data
    test_data = pd.read_csv(test_path, sep="\t", header=None)
    test_data.columns = ["id", "caption"]

    # Save IDs and raw image vectors separately but aligned
    ids = [i for i in train_images_vec]
    raw = np.array([train_images_vec[i] for i in train_images_vec])

    # Normalize image vectors to avoid normalized cosine and use dot
    raw = raw / np.array([np.sum(raw,1)] * raw.shape[1]).transpose()
    sim_test_results = {}

    for test_image in tqdm(test_data.id):
        # Get test image embedding
        image = Image.open(os.path.join(images_path, test_image))
        image = image.convert('RGB')
        vec = img2vec.get_vec(image)
        # Compute cosine similarity with every train image
        vec = vec / np.sum(vec)
        # Clone to do efficient mat mul dot
        test_mat = np.array([vec] * raw.shape[0])
        sims = np.sum(test_mat * raw, 1)
        top1 = np.argmax(sims)
        # Assign the caption of the most similar train image
        sim_test_results[test_image] = train_images[ids[top1]]

    # Save test results to tsv file
    df = pd.DataFrame.from_dict(sim_test_results, orient="index")
    df.to_csv(os.path.join(results_path, "onenn_results.tsv"), sep="\t", header=False)

    return sim_test_results