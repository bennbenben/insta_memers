### Import libraries ###
import cv2
import os
import argparse
from collections import defaultdict

### Helper functions ###

### Initialize variables ###
ig_defined_res = (1080.0, 1920.0)
resize_factor = .8
img_vars = defaultdict()

# file_path = "C:\\Users\\bennb\\Desktop\\yoda.jpg"


# Algo
# func 1. Read in image dimensions (esp width). Output a string: shrink or scale
# func 2. Resize according to pre-defined IG dimensions while maintaining aspect ratio (a percentage)
# func 3. Image padding

### Application functions ###
def shrink_or_scale(file_path: str, defined_res: tuple)->dict:
	"""
	Reads in an image and compares its width with a set of pre-defined resolutions
	Returns a dictionary of 2 key-value pairs: 
	{img_vars['img_obj']: cv2-read image object,
	img_vars['img_res']: (width as int, height int),
	img_vars['defined_res']: (width as int, height int),
	img_vars['resize_dir']: string}
	"""
	# Read image and load dimensions into img_vars dictionary
	img_vars['img_obj'] = cv2.imread(file_path)
	img_vars['img_res']= tuple(map(float,img_vars['img_obj'].shape[:2]))
	img_vars['defined_res'] = defined_res

	# Compare image width with pre-defined width
	if img_vars['img_res'][0] < img_vars['defined_res'][0]: img_vars['resize_dir'] = 'scale'
	else: img_vars['resize_dir'] = 'shrink'

	return img_vars

def image_resize(img_vars: dict, resize_factor: float)->dict:
	"""
	Takes in dictionary of image variables. Calculates and performs image resizing according to the element 'resize_dir' and 'resize_factor'
	If any of the resized dimension exceed that of defined dimension, then resize to the maximum of the limiting dimension, keeping aspect ratio constant

	"""
	img_vars['resize_factor']=resize_factor
	img_vars['resized_res']=tuple(i*resize_factor for i in img_vars['img_res'])

	return img_vars


### Application Main ###
if __name__=="__main__":

	# Parse arguments
	my_parser = argparse.ArgumentParser(prog="app_transform.py", description="Transform image to an easily readable format by both human and IG story", usage='%(prog)s "${strings_of_file_paths[@]}"')
	my_parser.add_argument("string_1", help="string: absolute path to image file. Use backslash for windows file paths", type=str, nargs="+")
	args=my_parser.parse_args()

	# Start Application
	for i in args.string_1:
		resize_direction=shrink_or_scale(i, ig_defined_res)
		# print(resize_direction)
		resize_result=image_resize(resize_direction, resize_factor)
		print(resize_result)
