### Import libraries ###
import cv2
import os
import argparse
from collections import defaultdict

### Helper functions ###

### Initialize variables ###
ig_defined_res = (1080.0, 1920.0) # give in a float value
screen_factor = .8
scale_tolerance=2
img_vars = defaultdict()

# Flow
# func 1. Read in image dimensions (esp width). Output a dictionary of variables to pass to func2
# func 2. Resize according to a percentage of pre-defined IG dimensions, while maintaining aspect ratio. Output a dictionary of variables to pass to func3
# func 3. Calculate the padding the images need and pass the variables to func4
# func 4. Execute the resize, and the image padding steps. Output the new image in a saved location

### Application functions ###
def resize_type(file_path: str, defined_res: tuple, screen_factor: float, scale_tolerance: float)->dict:
	"""
	Reads in an image and compares its width with a set of pre-defined resolutions
	Returns a dictionary of 2 key-value pairs: 
	{img_vars['img_obj']: cv2-read image object,
	img_vars['img_res']: (width as float, height as float),
	img_vars['img_aspect_ratio']: float,
	img_vars['defined_res']: (width as float, height float),
	img_vars['screen_factor']: float,
	img_vars['proposed_res']: (width as float, height as float),
	img_vars['proposed_resize_dir']: 'scale' or 'shrink' as string,
	img_vars['scale_tolerance']: float,
	img_vars['proposed_resize_factor']: float,
	img_vars['resize_validity']: boolean (None if proposed_resize_dir='shrink'. True/False if proposed_resize_dir='scale')}
	"""
	# Read image resolutions and aspect ratio, load these variables into img_vars dictionary
	img_vars['img_obj'] = cv2.imread(file_path)
	img_vars['img_res']= tuple(map(float,img_vars['img_obj'].shape[:2]))
	img_vars['img_aspect_ratio'] = img_vars['img_res'][0] / img_vars['img_res'][1]
	img_vars['defined_res'] = defined_res
	img_vars['screen_factor'] = screen_factor

	# Propose a resized image resolution (whether its scale or shrink)
	proposed_width = screen_factor * img_vars['defined_res'][0] # 1080 * 0.8 = 864
	proposed_height = proposed_width / img_vars['img_aspect_ratio'] # 864 / 0.8 = 1080

	if proposed_height <= defined_res[1]: pass
	else:
		proposed_height = screen_factor * img_vars['defined_res'][1]
		proposed_width = proposed_height * img_vars['img_aspect_ratio']

	img_vars['proposed_res'] = (proposed_width, proposed_height)
	if img_vars['proposed_res'][0] <= img_vars['img_res'][0] : img_vars['proposed_resize_dir'] = 'shrink'
	else: img_vars['proposed_resize_dir'] = 'scale'

	# Check if proposed resize is within specified tolerance
	img_vars['scale_tolerance'] = scale_tolerance
	img_vars['proposed_resize_factor'] = img_vars['proposed_res'][0] / img_vars['img_res'][0]

	if img_vars['proposed_resize_dir'] == 'scale':
		if img_vars['proposed_resize_factor'] <= img_vars['scale_tolerance']: img_vars['resize_validity'] = True
		else: img_vars['resize_validity'] = False

	if img_vars['proposed_resize_dir'] == 'shrink': img_vars['resize_validity'] = None

	return img_vars

def add_padding_vars(img_vars: dict)->dict:
	"""
	Takes in image varibles from resize_type function output in the form of a dictionary. Calculates the image padding and appends its details to the dictionary
	"""
	# Still development
	return

### Application Main ###
if __name__=="__main__":

	# Parse arguments
	my_parser = argparse.ArgumentParser(prog="app_transform.py", description="Transform image to an easily readable format by both human and IG story", usage='%(prog)s "${strings_of_file_paths[@]}"')
	my_parser.add_argument("string_1", help="string: absolute path to image file. Use backslash for windows file paths", type=str, nargs="+")
	args=my_parser.parse_args()

	# Start Application
	for i in args.string_1:
		resize_vars = resize_type(i, ig_defined_res, screen_factor, scale_tolerance)
		img_vars = add_padding_vars(resize_vars)
		
