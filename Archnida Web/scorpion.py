import sys
import os
from exif import Image


def CheckExtexion(Url):
    extention = os.path.splitext(Url)
    if (extention[1] == ".jpg" or extention[1] == ".jpeg" or extention[1] == ".png" or extention[1] == ".gif"  or extention[1] == ".bmp" ):
        return True
    else:
        return False


def PrintLst(lst_):

    print("-------------------------------")
    for link in lst_:
        print(link)
    print("-------------------------------")

def main(path):
    if CheckExtexion(path) is False:
        return
    print("---------------------------------")
    print("Opening image ->", path)
    with open(path, 'rb') as image_file:
        image_bytes = image_file.read()
    my_image = Image(image_bytes)
    print("Image has metadata ->", my_image.has_exif)
    if 'datetime_original' in dir(my_image):
        print("Taken on ", my_image.datetime_original)
    else:
        print("Taken on No data")
    if 'model' in dir(my_image):
        print("Taken with ->", my_image.model)
    else:
        print("Taken with ->  No data")
    if 'lens_model' in dir(my_image):
        print("Taken with lens ->", my_image.lens_model)
    else:
        print("Taken with lens ->  No data")
    if 'pixel_x_dimension' in dir(my_image) and 'pixel_y_dimension' in dir(my_image):
        print("Image resolution ->", my_image.pixel_x_dimension, "X", my_image.pixel_y_dimension)
    else:
        print("Image resolution -> No data")
    if 'gps_latitude' in dir(my_image):
        print("GPS latitude ->", my_image.gps_latitude)
    else:
        print("GPS latitude -> No data")
    if 'gps_longitude' in dir(my_image):
        print("GPS longitude ->", my_image.gps_longitude)
    else:
        print("GPS longitude -> No data")
    if 'exposure_time' in dir(my_image):
        print("Exposure time ->", my_image.exposure_time)
    else:
        print("Exposure time -> No data")
    if 'f_number' in dir(my_image):
        print("Aperture:f/", my_image.f_number)
    else:
        print("Aperture -> No data")
    if 'x_resolution' in dir(my_image) and 'y_resolution' in dir(my_image):
        print("Image DPI ->", my_image.x_resolution ,"*", my_image.y_resolution)
    else:
        print("Image DPI -> No data")

    print("---------------------------------")

if len(sys.argv) >= 2:
    for i in range(len(sys.argv)):
        main(sys.argv[i])
    sys.exit(1)
print("Please use: ./scorpion PATH")

