from google.cloud import vision
from google.cloud.vision import types
import io
import os
from PIL import Image
import argparse


# 画像の顔部分を切り取って保存する関数
def image_function(image,response,size,number,dir_name,people_name):
    if number == 0:
        make_dir = dir_name +'/resize/'
        if not os.path.exists(make_dir):
            os.makedirs(make_dir)
    im = Image.open(image)
    for face in response.face_annotations:
        number += 1
        print(face)
        box = [(vertex.x, vertex.y) for vertex in face.bounding_poly.vertices]
        box_for_trim = []
        taple_for_left = box[0]
        x = taple_for_left[0]
        y = taple_for_left[1] - 50
        if y < 0:
            y = 0
        taple_for_left = (x,y)
        taple = taple_for_left + box[2]
        print(taple)
        crop = im.crop(taple)
        resize = crop.resize(size)
        save_file_name = dir_name +'/resize/' + people_name + '_' +str(number)+'.jpg'
        print(str(save_file_name))
        resize.save(str(save_file_name))

    return number



# ディレクトリ内のファイル名をリストで返す関数
def file_enums(dir_name):
    return os.listdir(dir_name)


def main(dir_name,people_name,size):
    vision_client = vision.ImageAnnotatorClient()
    image = types.Image()
    number = 0
    file_list = file_enums(dir_name)
    print(file_list)
    for file_name in file_list:
        file_path = dir_name + '/' + file_name
        with io.open(file_path, 'rb') as image_file:
            content = image_file.read()
            image = types.Image(content=content)
            response = vision_client.face_detection(image = image)
            number = image_function(image_file,response,size,number,dir_name,people_name)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "description goes here")
    parser.add_argument("-d", type=str, help = "Write Directory Path", required=True)
    parser.add_argument("-n", type=str, help = "Write people name", required=True)
    args = parser.parse_args()
    dir_name = args.d
    people_name = args.n
    size = (64,64)
    main(dir_name,people_name,size)
