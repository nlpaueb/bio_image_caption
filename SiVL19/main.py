import create_vocabulary as vocab
import frequency_baseline as freq
import onenn_baseline as onenn
import wmd_evaluation as wmd
import create_json_files as json_file
import os

def main():

	#datasets paths
	PEIR_GROSS_PATH = "peir_gross/"
	IU_XRAY_PATH = "iu_xray/"
	#IMAGE_CLEF_PATH = "imageCLEF/"

	PEIR_GROSS_IMAGES_PATH = os.path.join(PEIR_GROSS_PATH, "peir_gross_images/")
	IU_XRAY_IMAGES_PATH = os.path.join(IU_XRAY_PATH, "iu_xray_images")
	#IMAGE_CLEF_IMAGES_PATH = "/home/cave-of-time/lion-o/BIO/data/i2t/imageCLEF2018/CaptionTraining2018/"

	#get statistics and create vocabulary for each dataset
	print("Processing Peir Gross:")
	peir_gross_length = vocab.create_vocabulary(PEIR_GROSS_PATH)
	print("Processing IU X-ray:")
	iu_xray_length = vocab.create_vocabulary(IU_XRAY_PATH)
	# print("Processing ImageCLEF:")
	# imageCLEF_length = vocab.create_vocabulary(IMAGE_CLEF_PATH)

	#run the frequency baseline for each dataset
	print("Frequency baseline for Peir Gross:")
	freq.most_frequent(PEIR_GROSS_PATH, peir_gross_length)
	print("Frequency baseline for IU X-ray:")
	freq.most_frequent(IU_XRAY_PATH, iu_xray_length)
	# print("Frequency baseline for ImageCLEF:")
	# freq.most_frequent(IMAGE_CLEF_PATH, imageCLEF_length)

	#run the onenn baseline for each dataset
	print("1NN baseline for Peir Gross:")
	onenn.most_similar(PEIR_GROSS_PATH, PEIR_GROSS_IMAGES_PATH)
	print("1NN baseline for IU X-ray:")
	onenn.most_similar(IU_XRAY_PATH, IU_XRAY_IMAGES_PATH)
	# print("1NN baseline for ImageCLEF:")
	# onenn.most_similar(IMAGE_CLEF_PATH, IMAGE_CLEF_IMAGES_PATH)

	#define pretrained embeddings path
	embeddings_path = "pubmed2018_w2v_200D/pubmed2018_w2v_200D.bin"

	#evaluate results with wmd
	print("Peir Gross evaluation:")
	wmd.evaluate(PEIR_GROSS_PATH, embeddings_path)
	print("IU X-ray evaluation:")
	wmd.evaluate(IU_XRAY_PATH, embeddings_path)
	# print("ImageCLEF evaluation:")
	# wmd.evaluate(IMAGE_CLEF_PATH, embeddings_path)

	#create json files for each dataset
	json_file.create_jsons(PEIR_GROSS_PATH)
	json_file.create_jsons(IU_XRAY_PATH)
	#json_file.create_jsons(IMAGE_CLEF_PATH)


if __name__ == "__main__":
	main()