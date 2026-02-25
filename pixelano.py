import re
import os
import sys
import shutil
from PIL import Image
import numpy as np
from shapely.geometry import MultiPoint

PIXELANO_INFO = """Pixelano - a simple image annotation tool, by Volodymyr \"Pravetz\" Didur"""

def generate_annotation(results, path, img_file, iwidth, iheight, idepth):
	with open(path, 'w', encoding='utf-8') as xmlf:
		xmlf.write(f"""<?xml version="1.0" encoding="utf-8"?>
<annotation>
	<folder/>
	<filename>{img_file}</filename>
	<path>{img_file}</path>
	<source></source>
	<size>
		<width>{iwidth}</width>
		<height>{iheight}</height>
		<depth>{idepth}</depth>
	</size>
	<segmented>0</segmented>""")
		
		for k, v in results.items():
			class_name = k.split('/')[0]
			
			xmlf.write(f"""
	<object>
		<name>{class_name}</name>
		<pose>Unspecified</pose>
		<truncated>0</truncated>
		<difficult>0</difficult>
		<occluded>0</occluded>
		<bndbox>
			<xmin>{int(v['bounding_box'][0])}</xmin>
			<xmax>{int(v['bounding_box'][2])}</xmax>
			<ymin>{int(v['bounding_box'][1])}</ymin>
			<ymax>{int(v['bounding_box'][3])}</ymax>
		</bndbox>
		<polygon>\n""")
			for i, point in enumerate(list(v['polygon'].exterior.coords)):
				xmlf.write(f"\t\t\t<x{i + 1}>{point[0]}</x{i + 1}>\n\t\t\t<y{i + 1}>{point[1]}</y{i + 1}>\n")
			xmlf.write(f"""\t\t</polygon>
	</object>""")
		
		xmlf.write("\n</annotation>")

def is_annotated(filename):
	image_name_noext = os.path.splitext(filename)[0]
	annotation_mark_pos = image_name_noext.rfind('_a')
	return annotation_mark_pos != -1 and annotation_mark_pos == len(image_name_noext) - 2

def find_image_by_name(directory, file_name):
	image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')
	for root, dirs, files in os.walk(directory):
		for file in files:
			base_name, ext = os.path.splitext(file)
			if base_name.lower() == file_name.lower() and ext.lower() in image_extensions and not is_annotated(file):
				return os.path.join(root, file)
	return None

def proc_image(path, ccm, output_path):
	print(f"proc {path}")
	image = Image.open(path).convert("RGB")
	img_array = np.array(image)
	results = {}
	
	for class_name, (color_lower, color_upper) in ccm.items():
		mask = np.all(
			(img_array >= color_lower) & (img_array <= color_upper), axis=-1
		)
		
		if not np.any(mask):
			print(f"No pixels found for class: {class_name}")
			continue
		
		unique_colors = np.unique(img_array[mask], axis=0)
		
		for color in unique_colors:
			color_mask = np.all(img_array == color, axis=-1)
			y_coords, x_coords = np.where(color_mask)
			
			coords = list(zip(x_coords, y_coords))
			
			if coords:
				polygon = MultiPoint(coords).convex_hull
				
				min_x, min_y, max_x, max_y = polygon.bounds
				
				instance_name = f"{class_name}/instance_{tuple(color)}"
				
				results[instance_name] = {
					"color": tuple(color),
					"polygon": polygon,
					"bounding_box": (min_x, min_y, max_x, max_y),
				}
			else:
				print(f"No coordinates for color {color} in class {class_name}")
	
	image_name = os.path.basename(path)
	image_name_unannotated = os.path.splitext(image_name)[0]
	annotation_mark_pos = image_name_unannotated.rfind('_a')
	if annotation_mark_pos != -1:
		image_name_unannotated = image_name_unannotated[: annotation_mark_pos]
	head, _ = os.path.split(path)
	image_file = find_image_by_name(head, image_name_unannotated)
	iwidth, iheight = image.size
	
	shutil.copyfile(image_file, os.path.join(output_path, os.path.basename(image_file)))
	generate_annotation(results, os.path.join(output_path, f"{image_name_unannotated}.xml"), os.path.basename(image_file), iwidth, iheight, len(image.mode))


def proc_directory(path, ccm, output_path):
	if not os.path.exists(path) or os.path.isfile(path):
		return
	
	basename = os.path.basename(path)
	temp_o = os.path.join(output_path, basename)
	
	if not os.path.exists(temp_o):
		os.makedirs(temp_o, exist_ok=True)
	
	for file in os.listdir(path):
		if not is_annotated(file):
			continue
		abs_path = os.path.join(path, file)
		proc_image(abs_path, ccm, temp_o)

def parse_rgb(string):
	return tuple(map(int, re.findall(r'\d+', string)))

def parse_class_color_map(path):
	ccm = {}
	
	with open(path, 'r', encoding='utf-8') as file:
		for line in file:
			tokens = line.strip().split('\t')
			ccm[tokens[0]] = [parse_rgb(tokens[1]), parse_rgb(tokens[2])]
			if len(ccm[tokens[0]][0]) != 3 or len(ccm[tokens[0]][1]) != 3:
				print("Color value for class needs to have exactly 3 channels(R, G, B)")
				exit()
	
	return ccm


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print(f"""{PIXELANO_INFO}\n\nUsage: {sys.argv[0]} <parameters>
	Possible parameters:
		-clm <path> = class to color map file path
			file needs to be filled with lines in following format:
				'<CLASS_NAME><TABULATION><LOWER RGB VALUE><TABULATION><UPPER RGB VALUE>', e.g. 'MyClass	220;0;0	255;0;0'
		-f <path> = specify path to single image file
			-f path/to/my/img.jpg
		-d <path> = specify path to directory with images
			-d path/to/my/images
		-o <path> = specify dataset output path""")
		exit()
	
	class_color_map_path = ""
	single_image_files = []
	directories = []
	output = ""
	
	i = 1
	while i < len(sys.argv):
		if sys.argv[i] == "-clm" and i + 1 < len(sys.argv):
			class_color_map_path = sys.argv[i + 1]
			i += 1
		elif sys.argv[i] == "-f" and i + 1 < len(sys.argv):
			single_image_files.append(sys.argv[i + 1])
			i += 1
		elif sys.argv[i] == "-d" and i + 1 < len(sys.argv):
			directories.append(sys.argv[i + 1])
			i += 1
		elif sys.argv[i] == "-o" and i + 1 < len(sys.argv):
			output = sys.argv[i + 1]
			i += 1
		
		i += 1
	
	if not class_color_map_path:
		print("Class to color map file path was not specified.")
		exit()
	if not single_image_files and not directories:
		exit()
	if not output:
		print("Output path was not specified.")
		exit()
	
	if not os.path.exists(output):
		os.makedirs(output)
	
	ccm = parse_class_color_map(class_color_map_path)
	
	for image in single_image_files:
		proc_image(image, ccm, output)
	
	for directory in directories:
		proc_directory(directory, ccm, output)