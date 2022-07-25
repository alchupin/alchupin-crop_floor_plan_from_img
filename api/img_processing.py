import os
import cv2
import numpy as np
from PIL import Image
from skimage.io import imread, imsave
from skimage.measure import label, regionprops
# from pdf2image import convert_from_path
# import filetype
import time
import math
from transliterate import translit

Image.MAX_IMAGE_PIXELS = 933120000
    

def get_file_name_and_path(file):
    return os.path.basename(file).split('.')[0], os.path.dirname(file)


def rotate_image(img, angle):
    im = Image.open(img)
    out = im.rotate(angle, expand=True)
    out.save('final_result.png')

# def create_jpeg_from_pdf(pdf_file_path):    
#     file_name_without_extension, file_path = get_file_name_and_path(pdf_file_path)
#     jpg_file = convert_from_path(pdf_file_path, 500)[0]
#     jpg_file.save(f'{file_path}/{file_name_without_extension}_JPEG.jpg', 'JPEG')


def get_image_area(image):     
    img = Image.open(image)
    height, width = img.size
    area = height * width
    return area


def crop_image(image_path, min_x, min_y, max_x, max_y, cropped_image_path):
    image = imread(image_path)
    cropped = image[min_x:max_x,min_y:max_y]
    imsave(cropped_image_path, cropped)

def delete_qr_code(image):
    img = cv2.imread(image)
    qr = cv2.QRCodeDetector().detect(img)
    if qr[0]:
        points = qr[1][0]

        for point in points:
            for coord in point:
                coord += 100
        points_array = np.array(points)

        cv2.fillPoly(img, pts = np.int32([points_array]), color=(255,255,255))
        image_qr_cut_name = f'{image}_qr_cut.jpg'
            
        cv2.imwrite(image_qr_cut_name, img)

        return (True, image_qr_cut_name)
    return (False, False)


def cut_floor_plan_from_image(image):
    qr_cut, path = delete_qr_code(image)
    if qr_cut:
        image = path  
    source_image_area = get_image_area(image)

    pim = Image.open(image)    
    pgr = pim.convert('L')
    thr = pgr.point(lambda p: p < 230 and 255)

    nim = np.array(thr)

    label_image=label(nim)
    # height, width = Image.open(image).size
    
    rp = regionprops(label_image)
    rp_less_then_image = [region for region in rp if region.bbox_area < source_image_area * 0.8]
    rp_sorted_80 = sorted(rp_less_then_image, key=lambda x: x.area, reverse=True)
    
    # rp_sorted_with_distance = sorted(rp_sorted, key=lambda x: math.dist(x.centroid, (height/2, width/2)))
    
    region = rp_sorted_80[0]
    min_x, min_y, max_x, max_y = region.bbox



    image_file_name, image_file_path = get_file_name_and_path(image)
    # result_files_dir = f'{image_file_path}/floor_plans'
    image_file_name = translit(image_file_name, 'ru', reversed=True)
    result_image_name = f'{image_file_name}_plan.png'

    crop_image(image, min_x, min_y, max_x, max_y, result_image_name)

    return os.path.basename(result_image_name)