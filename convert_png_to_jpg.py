import os
from PIL import Image
import pyheif
from tqdm import tqdm
import argparse


def check_size(image):
    width, height = image.size
    # print(width, height)
    #1024 x 768
    if width > 1024:
        new_width = 1024
        new_height = int(new_width*height/width)
    elif height > 1024:
        new_height = 1024
        new_width = int(new_height*width/height)
    else:
        new_width, new_height = width, height

    return (new_width, new_height)

def convert_image(fullpath, fname, do_resize):
    im = Image.open(fullpath)
    image = im.convert('RGB')
    
    if do_resize:
        new_dim = check_size(image)
        image = image.resize(new_dim,Image.ANTIALIAS)

    output_img_name = fname+'.jpg'
    #save image
    image.save(output_img_name, "JPEG")
    #remove png
    os.remove(fullpath) 

def main(args):
    
    input_directory = args.input_path
    do_resize = args.resize

    ext = ('.PNG', '.png')

    if args.subdirectories:
                
        for root,d_names,f_names in os.walk(input_directory):
            for f in tqdm(f_names):
                filepath = os.path.join(root, f)
                fname = os.path.splitext(filepath)[0]
                #check if extention is .PNG or .png
                fext = os.path.splitext(filepath)[1]
                if fext not in ext:
                    continue
                
                #convert image
                convert_image(filepath, fname, do_resize)
                

    else:
        
        for file in tqdm(os.listdir(input_directory)):
            fname = os.path.splitext(file)[0]
            fext = os.path.splitext(file)[1]
            if fext not in ext:
                continue
            filepath = os.path.join(input_directory, file)
            
            convert_image(filepath, fname, do_resize)
            
    
def parse_args():
    description = \
    '''
    This script can be used to batch convert heic to jpg.

    Usage:
    python3 convert_png_to_jpg.py 
        -i /fullpath/to/source/directory -r -s
    the command above will convert as well as resize the image to 1k
        if the image is 4k i.e. 4032 x 3024 this will be reduced to 1024 x 768
    
    '''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-i', '--input_path', action='store', help='absolute path to the heic images directory', required=True)
    parser.add_argument('-s', '--subdirectories', help='are the images in subdirectories?', required=False, action='store_true',  default=False)
    parser.add_argument('-r', '--resize', help='do you want to resize the image to 1k image?', required=False, action='store_true',  default=False)
            
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    main(args)