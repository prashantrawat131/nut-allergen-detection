from PIL import Image
import os
from torchvision import transforms

data = {
    "pure_peanut": {
        "start_index": 1,
        "end_index": 10,
        "x": 1776,
        "y": 604,
        "width": 2900,
        "height": 1400,
    },
    "wheat_peanut":
    {
        "start_index": 1,
        "end_index": 10,
        "x": 1660,
        "y": 3511,
        "width": 2900,
        "height": 1400,
    },
    "wheat_cashew":
    {
        "start_index": 1,
        "end_index": 10,
        "x": 1516,
        "y": 6145,
        "width": 2900,
        "height": 1400,
    },
    "pure_cashew":
    {
        "start_index": 11,
        "end_index": 20,
        "x": 703,
        "y": 1144,
        "width": 1400,
        "height": 2900,
    },
    "wheat_walnut":
    {
        "start_index": 11,
        "end_index": 20,
        "x": 3335,
        "y": 1472,
        "width": 1400,
        "height": 2900,
    },
    "pure_wheat":
    {
        "start_index": 11,
        "end_index": 20,
        "x": 6079,
        "y": 1564,
        "width": 1400,
        "height": 2900,
    },
    "wheat_almond": {
        "start_index": 21,
        "end_index": 30,
        "x": 1074,
        "y": 562,
        "width": 2900,
        "height": 1400,
    },
    "pure_almond": {
        "start_index": 21,
        "end_index": 30,
        "x": 1314,
        "y": 3447,
        "width": 2900,
        "height": 1400,
    },
    "pure_walnut": {
        "start_index": 21,
        "end_index": 30,
        "x": 1538,
        "y": 6153,
        "width": 2900,
        "height": 1400,
    },
    "wheat_almond_walnut": {
        "start_index": 31,
        "end_index": 40,
        "x": 2969,
        "y": 876,
        "width": 2276,
        "height": 941,
    },
    "wheat_almond_cashew": {
        "start_index": 31,
        "end_index": 40,
        "x": 3082,
        "y": 2716,
        "width": 2082,
        "height": 1010,
    },
    "wheat_almond_peanut": {
        "start_index": 31,
        "end_index": 40,
        "x": 3125,
        "y": 4264,
        "width": 2087,
        "height": 919,
    },
    "wheat_walnut_cashew": {
        "start_index": 31,
        "end_index": 40,
        "x": 3136,
        "y": 5971,
        "width": 2078,
        "height": 910,
    },
    "wheat_walnut_peanut": {
        "start_index": 31,
        "end_index": 40,
        "x": 1009,
        "y": 976,
        "width": 1040,
        "height": 2187,
    },
    "wheat_cashew_peanut": {
        "start_index": 31,
        "end_index": 40,
        "x": 1086,
        "y": 4261,
        "width": 876,
        "height": 1954,
    },
    "wheat_almond_cashew_peanut": {
        "start_index": 41,
        "end_index": 50,
        "x": 520,
        "y": 2004,
        "width": 967,
        "height": 2343,
    },
    "wheat_walnut_peanut_cashew": {
        "start_index": 41,
        "end_index": 50,
        "x": 2290,
        "y": 1994,
        "width": 1063,
        "height": 2345,
    },
    "wheat_almond_walnut_cashew": {
        "start_index": 41,
        "end_index": 50,
        "x": 4344,
        "y": 2022,
        "width": 1144,
        "height": 2246,
    },
    "all_mix":
    {
        "start_index": 51,
        "end_index": 60,
        "x": 2258,
        "y": 1330,
        "width": 1788,
        "height": 4719,
    },
}


transform_list = [
    transforms.RandomHorizontalFlip(
        p=1.0),               # 1. Flip horizontally
    transforms.RandomVerticalFlip(p=1.0),                 # 2. Flip vertically
    transforms.RandomRotation(degrees=45),                # 3. Rotate
    # 4. Brightness adjustment
    transforms.ColorJitter(brightness=0.5),
    # 5. Contrast adjustment
    transforms.ColorJitter(contrast=0.5),
    # 6. Random crop and resize
    transforms.RandomResizedCrop(size=(224, 224)),
    transforms.RandomAffine(degrees=0, translate=(0.2, 0.2)),  # 7. Translation
    # 8. Perspective distortion
    transforms.RandomPerspective(distortion_scale=0.5, p=1.0),
    transforms.GaussianBlur(kernel_size=5)                # 9. Blur
]


def extract_roi(image_source_path, x, y, width, height):
    with Image.open(image_source_path) as img:
        # crop box (left, upper, right, lower)
        crop_box = (x, y, x + width, y + height)

        # crop the image
        cropped_img = img.crop(crop_box)

        if cropped_img.height > cropped_img.width:
            cropped_img = cropped_img.rotate(90, expand=True)

        # resize image to (2800, 1400)
        cropped_img = cropped_img.resize((2800, 1400))

        return cropped_img


if not os.path.exists("./rgb_cropped_images"):
    os.makedirs("./rgb_cropped_images")


for key, value in data.items():
    start_index = value["start_index"]
    end_index = value["end_index"]
    x = value["x"]
    y = value["y"]
    width = value["width"]
    height = value["height"]
    # if not os.path.exists(f"./rgb_cropped_images/{key}"):
    #     os.makedirs(f"./rgb_cropped_images/{key}")
    image_number = 1
    image_sizes = [700, 512, 256]
    for i in range(start_index, end_index + 1):
        image_source_path = f"./RGB_samples/{i}.jpg"
        cropped_image = extract_roi(image_source_path, x, y, width, height)
        # divide the 2800, 1400 into 8 images of size 700, 700
        for j in range(4):
            for k in range(2):
                left = j * 700
                upper = k * 700
                right = left+700
                lower = upper+700
                cropped_img = cropped_image.crop((left, upper, right, lower))
                # print(
                #     f"left: {left}, upper: {upper}, right: {right}, lower: {lower}")
                for l in range(len(image_sizes)):
                    x_padding = (700 - image_sizes[l]) // 2
                    y_padding = (700 - image_sizes[l]) // 2
                    temp_img = cropped_img.crop((x_padding, y_padding, 700 - x_padding, 700 - y_padding))
                    if i % 10 != 9:
                        temp_img = transform_list[i % 10](temp_img)
                    image_path = f"./rgb_cropped_images/{image_sizes[l]}_{image_sizes[l]}/{key}/{image_number}.jpg"
                    if not os.path.exists(f"./rgb_cropped_images/{image_sizes[l]}_{image_sizes[l]}/{key}"):
                        os.makedirs(f"./rgb_cropped_images/{image_sizes[l]}_{image_sizes[l]}/{key}")
                    temp_img.save(image_path)
                    image_number += 1
        print(f"Processed {key} {i} image")
