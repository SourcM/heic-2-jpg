import os
import cv2
import random
import shutil
from tqdm import tqdm
import argparse

EXTs = ('jpg', 'JPG', 'jpeg', 'JPEG')


def colorjitter(img, cj_type="b"):
    print(img.shape)
    '''
    ### Different Color Jitter ###
    img: image
    cj_type: {b: brightness, s: saturation, c: constast}
    '''
    if cj_type == "b":
        # value = random.randint(-50, 50)
        value = np.random.choice(np.array([-50, -40, -30, 30, 40, 50]))
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        if value >= 0:
            lim = 255 - value
            v[v > lim] = 255
            v[v <= lim] += value
        else:
            lim = np.absolute(value)
            v[v < lim] = 0
            v[v >= lim] -= np.absolute(value)

        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        return img
    
    elif cj_type == "s":
        # value = random.randint(-50, 50)
        value = np.random.choice(np.array([-50, -40, -30, 30, 40, 50]))
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        if value >= 0:
            lim = 255 - value
            s[s > lim] = 255
            s[s <= lim] += value
        else:
            lim = np.absolute(value)
            s[s < lim] = 0
            s[s >= lim] -= np.absolute(value)

        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        return img
    
    elif cj_type == "c":
        brightness = 10
        contrast = random.randint(40, 100)
        dummy = np.int16(img)
        dummy = dummy * (contrast/127+1) - contrast + brightness
        dummy = np.clip(dummy, 0, 255)
        img = np.uint8(dummy)
        return img

def noisy(img, noise_type="gauss"):
    '''
    ### Adding Noise ###
    img: image
    cj_type: {gauss: gaussian, sp: salt & pepper}
    '''
    if noise_type == "gauss":
        image=img.copy() 
        mean=0
        st=0.7
        gauss = np.random.normal(mean,st,image.shape)
        gauss = gauss.astype('uint8')
        image = cv2.add(image,gauss)
        return image
    
    elif noise_type == "sp":
        image=img.copy() 
        prob = 0.05
        if len(image.shape) == 2:
            black = 0
            white = 255            
        else:
            colorspace = image.shape[2]
            if colorspace == 3:  # RGB
                black = np.array([0, 0, 0], dtype='uint8')
                white = np.array([255, 255, 255], dtype='uint8')
            else:  # RGBA
                black = np.array([0, 0, 0, 255], dtype='uint8')
                white = np.array([255, 255, 255, 255], dtype='uint8')
        probs = np.random.random(image.shape[:2])
        image[probs < (prob / 2)] = black
        image[probs > 1 - (prob / 2)] = white
        return image


def main(args):
    pp = args.input_path
    dpp = args.output_path
    test_perc = args.percentage_v

    #iterate through image directories
    for folder in tqdm(os.listdir(pp)):
        #get full folder path
        folderpath = os.path.join(pp, folder)

        #add images into list
        imgs = []
        for file in os.listdir(folderpath):
            fullfile = os.path.join(folderpath, file)
            if file.endswith(EXTs):
                imgs.append(fullfile)

        #get validation images and train images
        ff = int(round(len(imgs)*test_perc))
        train_imgs = imgs[:-ff]
        val_imgs = imgs[-ff:]

        #move images if val_imgs list is not empty
        #make destination dir
        dpp_path = os.path.join(dpp, folder)
        if not os.path.exists(dpp_path):
            # Create a new directory to save val images
            os.makedirs(dpp_path)
        if val_imgs:
            for file in val_imgs:
                #move to destination
                shutil.move(file, os.path.join(dpp_path, os.path.basename(file)))
        else: #val_imgs list is empty getone from train_imgs
            val_img = train_imgs[-1:]
            shutil.move(val_img, os.path.join(dpp_path, os.path.basename(val_img)))
            #reduce train_imgs list appropriately
            train_imgs = train_imgs[:-1]
        if len(train_imgs) < 4:
            #augment and save in training directory
            for i, file in enumerate(train_imgs):
                img = cv2.imread(file) 
                #randomy call one of two functions
                num1 = random.randint(1, 2)
                if num1 == 1:
                    im = colorjitter(img)
                else:
                    im = noisy(img)
                #save
                new_path = os.path.join(os.path.dirname(file), str(i)+'_'+os.path.basename(file))
                cv2.imwrite(new_path, im)

def parse_args():
    description = \
    '''
    This script can be used to go through directories and split train and test.
    Usage:
    python3 split_train_and_test_data.py 
        -i /fullpath/to/source/directory -o /fullpath/to/val/directory -p
    
    it is assumed images for different classes are grouped in sub directories
    
    '''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-i', '--input_path', action='store', help='absolute path to the input directory', required=True)
    parser.add_argument('-o', '--output_path', action='store', help='absolute path to the output directory', required=True)
    parser.add_argument('-p', '--percentage_v', help='What percentage of the data will be used as validation data', required=False, type=float, choices=Range(0.0, 1.0),  default=0.2)
            
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    main(args)
    