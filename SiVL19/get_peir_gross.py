import os
import requests
from shutil import rmtree
from bs4 import BeautifulSoup
import random
import numpy
import json

def split_images(images, keys, filename):
	new_images = {}

	for key in keys:
		new_images[key] = images[key]

	with open(filename, "w") as output_file:
		for new_image in new_images:
			output_file.write(new_image + "\t" + new_images[new_image])
			output_file.write("\n")


base_url = "http://peir.path.uab.edu/library"

# create dataset and images folder
try:
	rmtree("peir_gross/peir_gross_images/")
except BaseException:
	pass
os.makedirs("peir_gross/peir_gross_images/")

image_captions = {}
image_tags = {}

# the main page of the pathology category that contains the collections of all the sub-categories
main_page_url = "http://peir.path.uab.edu/library/index.php?/category/2"
main_page = requests.get(main_page_url)
soup = BeautifulSoup(main_page.content, "html.parser")

# find the links for each sub-category
categories = soup.find("li", class_="selected").find_all("li")
categories_urls = [category.find("a").get("href") for category in categories]

# go to each sub-category and extract images from the Gross sub-collection
for url in categories_urls:
	i = 1
	image_sum = 0

	category_url = base_url + "/" + url
	category_page = requests.get(category_url)
	category_soup = BeautifulSoup(category_page.content, "html.parser")

	# find the Gross sub-collection, if it exists
	collections_urls = {}
	collections = category_soup.find("li", class_="selected").find_all("li")
	for collection in collections:
		name = collection.find("a").get_text()
		collection_url = collection.find("a").get("href")
		collections_urls[name] = collection_url

	if "Gross" in list(collections_urls.keys()):
		# the page of Gross sub-collection to start extracting images from
		page_url = base_url + "/" + collections_urls["Gross"]

		page = requests.get(page_url)
		page_soup = BeautifulSoup(page.content, "html.parser")

		# the url of the last page or empty if there is only one page
		last_page = page_soup.find("a", rel="last")
		if last_page is None:
			last_page_url = ""
		else:
			last_page_url = base_url + "/" + last_page.get("href")

		# get the images from all the pages
		while True:

			# find the links to the images of the current page
			thumbnails = page_soup.find("ul", class_="thumbnails").find_all("a")

			for thumbnail in thumbnails:
				# get the image url
				image_url = base_url + "/" + thumbnail.get("href")
				# go to the image page and extract the data
				image_page = requests.get(image_url)
				image_soup = BeautifulSoup(image_page.content, "html.parser")

				image = image_soup.find("img", id="theMainImage")
				filename = image.get("alt")
				image_src = image.get("src")
				description = image.get("title").replace("\r\n", " ")
				image_captions[filename] = description

				tags_container = image_soup.find("div", {"id":"Tags"})
				tags = [tag.string for tag in tags_container.findChildren("a")]
				image_tags[filename] = tags

				# save the image to images folder
				with open( "peir_gross/peir_gross_images/" + filename, "wb") as f:
					image_file = requests.get(base_url + "/" + image_src)
					f.write(image_file.content)

			print("Extracted", len(thumbnails), "image-caption pairs from page", i)
			image_sum = image_sum + len(thumbnails)
			i += 1

			# if the current page is the last page stop
			if page_url == last_page_url or last_page_url == "":
				print("This was the last page")
				break

			# go to the next page
			page_url = base_url + "/" + page_soup.find("a", rel="next").get("href")
			page = requests.get(page_url)
			page_soup = BeautifulSoup(page.content, "html.parser")

		print("Visited", i-1, "pages of Gross sub-collection")
		print("Extracted", image_sum, "image-caption pairs from the", category_soup.find("li", class_="selected").find("a").get_text(), "category")


with open("peir_gross/peir_gross.tsv", "w") as output_file:
	for image in image_captions:
		output_file.write(image + "\t" + image_captions[image])
		output_file.write("\n")

# JSON saving
with open("peir_gross/peir_gross_captions.json", "w") as output_file:
    output_file.write(json.dumps(image_captions))
with open("peir_gross/peir_gross_tags.json", "w") as output_file:
    output_file.write(json.dumps(image_tags))


print("Wrote all", len(image_captions), "image-caption pairs to tsv.")

# split to train and test
random.seed(42)
keys = list(image_captions.keys())
random.shuffle(keys)

train_split = int(numpy.floor(len(image_captions) * 0.9))

train_keys = keys[:train_split]
test_keys = keys[train_split:]

split_images(image_captions, train_keys, "peir_gross/train_images.tsv")
split_images(image_captions, test_keys, "peir_gross/test_images.tsv")