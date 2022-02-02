### Import libraries ###
import cv2
import os
import argparse
from collections import defaultdict
import numpy as np

### Helper functions ###

### Initialize variables ###
ig_defined_res = (1920, 1080) # IG story max screen resolution. Use height x width as opencv follows numpy orientation
screen_factor = .83339274 # float
scale_tolerance = 2 # for resizing - only scale
img_vars = defaultdict()
output_file="C:\\Users\\bennb\\Desktop\\formatted_1.jpg"

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
	img_vars['img_res']= img_vars['img_obj'].shape[:2] # returns height, width, channels
	img_vars['img_aspect_ratio'] = float(img_vars['img_res'][1]) / float(img_vars['img_res'][0])
	img_vars['defined_res'] = defined_res
	img_vars['screen_factor'] = screen_factor

	# Propose a resized image resolution (whether its scale or shrink)
	## Scale width and check if height is acceptable
	proposed_width = int(screen_factor * float(img_vars['defined_res'][1])) # 1080 * 0.8 = 864
	proposed_height = int(float(proposed_width) / img_vars['img_aspect_ratio']) # 864 / 0.8 = 1080

	if proposed_height <= defined_res[0]: pass

	## If height is unacceptable, scale height and width will change accordingly
	else:
		proposed_height = int(screen_factor * float(img_vars['defined_res'][0]))
		proposed_width = int(float(proposed_height) * img_vars['img_aspect_ratio'])

	img_vars['proposed_res'] = (proposed_height,proposed_width)

	# Get resize direction: 'scale' or 'shrink' by comparing width (height is also acceptable; but both yield same values)
	if img_vars['proposed_res'][1] <= img_vars['img_res'][1] : img_vars['proposed_resize_dir'] = 'shrink' 
	else: img_vars['proposed_resize_dir'] = 'scale'

	# Check if proposed resize is within specified tolerance
	img_vars['scale_tolerance'] = scale_tolerance
	img_vars['proposed_resize_factor'] = int(float(img_vars['proposed_res'][1]) / float(img_vars['img_res'][1]))

	if img_vars['proposed_resize_dir'] == 'scale':
		if img_vars['proposed_resize_factor'] <= img_vars['scale_tolerance']: img_vars['resize_validity'] = True
		else: img_vars['resize_validity'] = False

	elif img_vars['proposed_resize_dir'] == 'shrink': img_vars['resize_validity'] = None

	return img_vars

def add_pip_vars(img_vars: dict)->dict:
	"""
	Input: takes in output from resize_type function in the form of a dictionary
	Performs: (1) Calculates the Picture-in-Picture (PIP) details, (2) Loads the canvas, (3) Appends the PIP details and canvas object to the dictionary
	Output: outputs the appended dictionary
	"""
	# Read the pre-defined dictionary dimensions and create a canvas of fixed color. Append it to the dictionary
	height, width = img_vars['defined_res']
	# blank_image = np.zeros((height,width,3), dtype=np.uint8) # creates a black image
	colored_image = np.full(shape=(height, width, 3), fill_value=128, dtype=np.uint8) # creates an gray canvas. RGB colour for grey is (128, 128, 128)  
	img_vars['canvas'] = colored_image

	# Get coordinates of resized image on canvas
	y1, x1 = map(int,(np.asarray(img_vars['defined_res']) - np.asarray(img_vars['proposed_res']))/2)
	x2 = x1 + img_vars['proposed_res'][1]
	y2 = y1 + img_vars['proposed_res'][0]

	img_vars['pip_coords'] = {'x1':x1,'x2':x2,'y1':y1,'y2':y2}

	return img_vars

def process_image(img_vars: dict, output_file: str)->dict:
	"""
	Input: (1) Reads the dictionary of image objects and variables, (2) Output file location
	Performs: (1) Image resizing, (2) Pasting resized image into canvas object, (3) Saves the processed image into the output file location
	Output: None
	"""
	# Image resizing
	resized_img = cv2.resize(img_vars['img_obj'], (img_vars['proposed_res'][1], img_vars['proposed_res'][0]))
	print('Checkpoint. Resized image dimensions: height={0}, width={1}, channels={2}'.format(resized_img.shape[0], resized_img.shape[1], resized_img.shape[2]))

	# Make a copy of the canvas and paste the resized image inside
	processed_img = img_vars['canvas']
	print('Checkpoint. New canvas dimensions: height={0}, width={1}, channels={2}'.format(processed_img.shape[0], processed_img.shape[1], processed_img.shape[2]))

	processed_img[img_vars['pip_coords']['y1']:img_vars['pip_coords']['y2'], img_vars['pip_coords']['x1']:img_vars['pip_coords']['x2']]=resized_img

	# Write the processed image to file destination
	cv2.imwrite(output_file, processed_img)

	return img_vars

### Application Main ###
if __name__=="__main__":

	# Parse arguments
	my_parser = argparse.ArgumentParser(prog="app_transform.py", description="Transform image to an easily readable format by both human and IG story", usage='%(prog)s "${strings_of_file_paths[@]}"')
	my_parser.add_argument("string_1", help="string: absolute path to image file. Use backslash for windows file paths", type=str, nargs="+")
	args=my_parser.parse_args()

	# Start Application
	for i in args.string_1:
		resized_img_vars = resize_type(i, ig_defined_res, screen_factor, scale_tolerance)
		pip_img_vars = add_pip_vars(resized_img_vars)
		processed_img_vars = process_image(pip_img_vars, output_file)
