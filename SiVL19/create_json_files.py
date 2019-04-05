import json
import os

def load_tsv(filename):
	images = {}

	with open(filename, "r") as file:
		for line in file:
			line = line.replace("\n", "").split("\t")
			images[line[0]] = line[1]

	return images


def create_json_gts(gts_name, images):
	ann_feeds = []
	img_feeds = []

	for image in images:
		img_entry= {'id': image.replace(".jpg", "").replace(".png", ""), 'file_name': image}
		img_feeds.append(img_entry)

	#create json file for images
	fileImagesName = './images.json'

	with open(fileImagesName, 'w') as f:
		json.dump([],f) 
	with open(fileImagesName, 'w') as fp:
		json.dump( img_feeds , fp , separators=(', ',': ') )

	#create json file for captions
	fileReportsName = './captions.json'

	for image in images:
		entry= {'image_id': image.replace(".jpg", "").replace(".png", ""), 'id': list(images.keys()).index(image) , 'caption': images[image]}
		ann_feeds.append(entry)

	with open(fileReportsName, 'w') as f:
		json.dump([],f) 
	with open(fileReportsName, 'w') as fp:
		json.dump( ann_feeds , fp , separators=(', ',': ') )

	with open(fileReportsName) as f:
		captions_data = json.load(f)
				
	with open(fileImagesName) as f:
		images_data = json.load(f)
			
	ann_entry = { 'images' : images_data, 'annotations' : captions_data, 'type' : "", 'categories' : "", 'info' : "", 'licenses' : ""}

	with open(gts_name, 'w') as f:
		json.dump({},f) 
	with open(gts_name, 'w') as fp:
		json.dump( ann_entry , fp , separators=(', ',': ') )

	os.system("rm " + fileImagesName)
	os.system("rm " + fileReportsName)


def create_json_res(res_name, images):

	res_feeds = []

	for image in images:
		entry= {'image_id': image.replace(".jpg", "").replace(".png", ""), 'caption': images[image]}
		res_feeds.append(entry)

	with open(res_name, 'w') as f:
		json.dump([],f) 
	with open(res_name, 'w') as fp:
		json.dump( res_feeds , fp , separators=(', ',': ') )


def create_jsons(filepath):

	gts = load_tsv(os.path.join(filepath, "test_images.tsv"))
	freq_results = load_tsv(os.path.join(filepath, "freq_results.tsv"))
	onenn_results = load_tsv(os.path.join(filepath, "onenn_results.tsv"))

	gts_json = os.path.join(filepath, "test_images.json")
	freq_json = os.path.join(filepath, "freq_results.json")
	onenn_json = os.path.join(filepath, "onenn_results.json")

	create_json_gts(gts_json, gts)
	create_json_res(freq_json, freq_results)
	create_json_res(onenn_json, onenn_results)
