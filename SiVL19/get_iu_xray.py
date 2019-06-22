import os
from shutil import rmtree
import xml.etree.ElementTree as ET
import random
import numpy
import json

def split_cases(reports_images, reports_text, keys, filename):
	new_images = {}

	for key in keys:
		for image in reports_images[key]:
			new_images[image] = reports_text[key]

	with open(filename, "w") as output_file:
		for new_image in new_images:
			output_file.write(new_image + "\t" + new_images[new_image])
			output_file.write("\n")

# create dataset folder
try:
	rmtree("iu_xray/")
except BaseException:
	pass
os.makedirs("iu_xray/")

# download PNG images
os.system("wget -P iu_xray/ https://openi.nlm.nih.gov/imgs/collections/NLMCXR_png.tgz")

# download reports
os.system("wget -P iu_xray/ https://openi.nlm.nih.gov/imgs/collections/NLMCXR_reports.tgz")

# create folder for images
os.makedirs("iu_xray/iu_xray_images/")

# unzip
os.system("tar -xzf ./iu_xray/NLMCXR_png.tgz -C iu_xray/iu_xray_images/")
os.system("tar -xzf ./iu_xray/NLMCXR_reports.tgz -C iu_xray/")

# read the reports xml files and create the dataset tsv
reports_path = "iu_xray/ecgen-radiology"

reports = os.listdir(reports_path)

reports.sort()

reports_with_no_image = []
reports_with_empty_sections = []
reports_with_no_impression = []
reports_with_no_findings = []

images_captions = {}
images_major_tags = {}
images_auto_tags = {}
reports_with_images = {}
text_of_reports = {}

for report in reports:

	tree = ET.parse(os.path.join(reports_path, report))
	root = tree.getroot()
	img_ids = [] 
	# find the images of the report
	images = root.findall("parentImage")
	# if there aren't any ignore the report
	if len(images) == 0:
		reports_with_no_image.append(report)
	else:

		sections = root.find("MedlineCitation").find("Article").find("Abstract").findall("AbstractText")
		# find impression and findings sections
		for section in sections:
			if section.get("Label") == "FINDINGS":
				findings = section.text
			if section.get("Label") == "IMPRESSION":
				impression = section.text

		if impression is None and findings is None:
			reports_with_empty_sections.append(report)
		else:
			if impression is None:
				reports_with_no_impression.append(report)
				caption = findings
			elif findings is None:
				reports_with_no_findings.append(report)
				caption = impression
			else:
				caption = impression + " " + findings

			# get the MESH tags
			tags = root.find("MESH")
			major_tags = []
			auto_tags = []
			if len(tags)>0:
				major_tags = tags.findall("major")
				auto_tags = tags.finall("automatic")

			for image in images:
				iid = image.get("id") + ".png"
				images_captions[iid] = caption
				img_ids.append(iid)
				images_major_tags[iid] = major_tags
				images_auto_tags[iid] = auto_tags

			reports_with_images[report] = img_ids
			text_of_reports[report] = caption


print("Found", len(reports_with_no_image), "reports with no associated image")
print("Found", len(reports_with_empty_sections), "reports with empty Impression and Findings sections")
print("Found", len(reports_with_no_impression), "reports with no Impression section")
print("Found", len(reports_with_no_findings), "reports with no Findings section")

print("Collected", len(images_captions), "image-caption pairs")

with open("iu_xray/iu_xray.tsv", "w") as output_file:
	for image_caption in images_captions:
		output_file.write(image_caption + "\t" + images_captions[image_caption])
		output_file.write("\n")

# Safer JSON storing
with open("iu_xray/iu_xray_captions.json", "w") as output_file:
	output_file.write(images_captions)
with open("iu_xray/iu_xray_tags.json", "w") as output_file:
	output_file.write(images_major_tags)


# perform a case based split
random.seed(42)
keys = list(reports_with_images.keys())
random.shuffle(keys)

train_split = int(numpy.floor(len(reports_with_images) * 0.9))

train_keys = keys[:train_split]
test_keys = keys[train_split:]

train_path = "iu_xray/train_images.tsv"
test_path = "iu_xray/test_images.tsv"

split_cases(reports_with_images, text_of_reports, train_keys, train_path)
split_cases(reports_with_images, text_of_reports, test_keys, test_path)