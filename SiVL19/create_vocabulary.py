import re
import os


def create_vocabulary(filepath, results_path):
    """
    Creates vocabulary of unique words and computes statistics for the train captions

    :param filepath: The path to the train data tsv file with the form: "image \t caption"
    :param results_path: The folder in which to save the vocabulary file
    :return: The average caption length
    """

    # Clean for BioASQ
    bioclean = lambda t: re.sub('[.,?;*!%^&_+():-\[\]{}]', '',
                                t.replace('"', '').replace('/', '').replace('\\', '')
                                .replace("'",'').strip().lower()).split()


    total_words = []
    pr_captions = []

    # Read data
    with open(filepath, "r") as file:

        for line in file:
            line = line.replace("\n", "").split("\t")

            # Apply bioclean to the caption
            tokens = bioclean(line[1])
            for token in tokens:
                total_words.append(token)
            caption = " ".join(tokens)
            pr_captions.append(caption)


    print("Total number of captions is",len(pr_captions))

    # Find the unique captions in the train data
    unique_captions = set(pr_captions)
    print("Total number of unique captions is", len(unique_captions))

    # Compute the mean caption length
    mean_length = len(total_words)/len(pr_captions)
    print("The average caption length is", mean_length, "words")

    # Create vocabulary of unique words
    vocabulary = set(total_words)
    print("Unique words are", len(vocabulary))
    # Save vocabulary file to dataset folder
    with open(os.path.join(results_path, "vocabulary.txt"), 'w') as output_file:
        for word in vocabulary:
            output_file.write(word)
            output_file.write("\n")
    

    return mean_length
