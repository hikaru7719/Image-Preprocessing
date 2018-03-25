from google.cloud import vision
from google.cloud.vision import types
import io
import os
from PIL import Image
import argparse


def image_function(image,size,file_path):
    im = Image.open(image)
    resize = im.resize(size)
    rotate = resize.rotate(-90)
    rotate.save(str(file_path))


def file_enums(dir_name):
    return os.listdir(dir_name)

def main(dir_name,size):
    file_list = file_enums(dir_name)
    number = 32
    print(file_list)
    for file_name in file_list:
        file_path = dir_name + '/' + file_name
        with io.open(file_path, 'rb') as image_file:
            content = image_file.read()
            number -= 1
            if number > 0:
                image_function(image_file,size,file_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "description goes here")
    parser.add_argument("-d", type=str, help = "Write Directory Path", required=True)
    args = parser.parse_args()
    dir_name = args.d
    size = (1600,1200)
    main(dir_name,size)
