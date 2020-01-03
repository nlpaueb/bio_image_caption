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


def download_iu_xray():
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


def parse_reports(reports_path):
    """

    :param reports_path: The path to the ecgen-radiology folder that contains the xml files
    :return: A dictionary that has the xml filenames as keys and as values dictionaries with the sections
            of the reports: Images, Comparison, Indication, Findings, Impression, Mti tags, Manual tags
    """

    # read the reports xml files and create the dataset tsv
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

    full_reports = {}

    for report in reports:

        comparison = ""
        indication = ""
        findings = ""
        impression = ""

        img_ids = []
        mti_tags = []
        manual_tags = []

        tree = ET.parse(os.path.join(reports_path, report))
        root = tree.getroot()

        # find the images of the report
        images = root.findall("parentImage")
        # if there aren't any ignore the report
        if len(images) == 0:
            reports_with_no_image.append(report)
        else:
            sections = root.find("MedlineCitation").find("Article").find("Abstract").findall("AbstractText")
            # get the sections of the reports
            for section in sections:
                if section.get("Label") == "COMPARISON":
                    comparison = section.text
                if section.get("Label") == "INDICATION":
                    indication = section.text
                if section.get("Label") == "FINDINGS":
                    findings = section.text
                if section.get("Label") == "IMPRESSION":
                    impression = section.text

            # get MTI and Manually generated tags
            tags = root.find("MeSH")
            if tags is not None:
                manual_tags = [t.text for t in tags.findall("major")]
                mti_tags = [t.text for t in tags.findall("automatic")]

            # get the image ids of the report
            for image in images:
                image_id = image.get("id") + ".png"
                img_ids.append(image_id)


            full_reports[report] = {"Images": img_ids, "Comparison": comparison, "Indication": indication,
                                    "Findings": findings, "Impression": impression,
                                    "MTI tags": mti_tags, "Manual tags": manual_tags}


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


                for iid in img_ids:
                    images_captions[iid] = caption
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
        output_file.write(json.dumps(images_captions))
    with open("iu_xray/iu_xray_major_tags.json", "w") as output_file:
        output_file.write(json.dumps(images_major_tags))
    with open("iu_xray/iu_xray_auto_tags.json", "w") as output_file:
        output_file.write(json.dumps(images_auto_tags))

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

    return full_reports
