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

def convert_image(fullpath, do_resize):
    heif_file = pyheif.read(fullpath)
    image = Image.frombytes(
        heif_file.mode, 
        heif_file.size, 
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
        )

    if do_resize:
        new_dim = check_size(image)
        image = image.resize(new_dim,Image.ANTIALIAS)

    return image

def main(args):
    
    input_directory = args.input_path
    output_directory = args.output_path
    do_resize = args.resize
    exts = ('.HEIC', '.heic')

    if args.subdirectories:

        for root,d_names,f_names in os.walk(input_directory):
            for f in tqdm(f_names):
                filepath = os.path.join(root, f)
                fname = os.path.splitext(os.path.basename(filepath))[0]

                fext = os.path.splitext(os.path.basename(filepath))[1]
                if fext not in exts:
                    continue

                dirname = os.path.dirname(filepath)
                subdirname = os.path.basename(os.path.dirname(filepath))
                output_subdir = os.path.join(output_directory, subdirname)

                #create subdirectory in destination if it doesn't exist
                if not os.path.exists(output_subdir):
                    os.makedirs(output_subdir)
                #convert image
                image = convert_image(filepath, do_resize)
                output_img_name = os.path.join(output_subdir, fname+'.jpg')
                #save image
                image.save(output_img_name, "JPEG")

    else:
        
        for file in tqdm(os.listdir(input_directory)):
            fname = os.path.splitext(file)[0]
            fullpath = os.path.join(input_directory, file)

            fext = os.path.splitext(file)[1]
            if fext not in exts:
                continue
            
            image = convert_image(fullpath, do_resize)
            output_img_name = os.path.join(output_directory, fname+'.jpg')
            #save image
            image.save(output_img_name, "JPEG")
    
def parse_args():
    description = \
    '''
    This script can be used to batch convert heic to jpg.

    Usage:
    python3 convert_heic_to_jpg.py 
        -i /fullpath/to/source/directory -o /fullpath/to/destination/directory -r
    the command above will convert as well as resize the image to 1k
        if the image is 4k i.e. 4032 x 3024 this will be reduced to 1024 x 768
    
    '''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-i', '--input_path', action='store', help='absolute path to the heic images directory', required=True)
    parser.add_argument('-o', '--output_path', action='store', help='absolute path to the jpg images directory', required=True)
    parser.add_argument('-s', '--subdirectories', help='are the images in subdirectories?', required=False, action='store_true',  default=False)
    parser.add_argument('-r', '--resize', help='do you want to resize the image to 1k image?', required=False, action='store_true',  default=False)
            
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    main(args)
