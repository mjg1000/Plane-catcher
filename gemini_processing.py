from google import genai
from google.genai import types
from keys import keyStore
from PIL import Image, ImageDraw, ImageFont
import json
import io
import os
import time
# Configure the API key





class gemini_components():
    def __init__(self):
        store = keyStore() 
        store.add_gemini_key()
        gemini_key = store.keys["gemini"]

        self.client = genai.Client(api_key = gemini_key)
        self.models = ["gemini-2.5-flash", "gemma-3-27b-it", "gemma-3-12b-it", "gemini-3-flash-preview", "gemini-2.5-flash-lite"]
        self.model_choices = {"check":1, "extract":1, "box":0}
        print("model check:",self.models[self.model_choices['check']],"model extract:",self.models[self.model_choices['extract']],"model box:",self.models[self.model_choices['box']])

    def request_gemini(self, image_bytes, im_type, name):
        if im_type == "jpg":
            im_type = "jpeg"
        first_answer =  self.bounding_box(image_bytes, im_type, name)
        print("checked:", first_answer)
        if first_answer == 0:
            return "Tail number not identifiable"
        elif first_answer == 1:
            return "Tail number too low quality"
        else:
            image = first_answer
        buffer = io.BytesIO()
        image.save(buffer, format=im_type.upper())  # or "PNG", "WEBP"
        image_bytes = buffer.getvalue()

        time.sleep(2.5) # rate limit fix
        tail = self.request_gemini_extract(image_bytes, im_type)
        
        if "Tail number: " in tail:
            tail = tail.split("Tail number: ")[1]
        return tail
    

        
    def request_gemini_extract(self, image_bytes, im_type):
        # Get the response text
        model = self.model_choices['extract']
        model = self.models[model]
        prompt = """
        You will be given an image with a red box. The image is of a plane, and inside the red box is the plane's tail number.
        Determine based *ONLY* on the contents of the image and no external information if: 1) if the tail number is visible and legible, 2) what the tail number is. Then, respond according to the following rules:
            If the tail number isnt shown in the image or if the image is too low quality to read the tail number:
                'Error: Tail Number Not Visible'
            if tail number is partially obscured / the image quality is not good enough to make out some digits:
                'Tail number: <Tail number with obscured/low confidence characters replaced with '*', e.g. G-*LM*P>'
            If and only if tail number *fully* visible:
                'Tail number: <Tail number, e.g. G-HLMOP>'
        You should respond in exactly this format, with no other text.
        """
        response = self.client.models.generate_content(
            model=model,
            contents=[
                types.Part.from_bytes(
                data=image_bytes,
                mime_type='image/'+im_type,
                ),
                prompt
            ]
        )
        txt = response.text
        return txt 
    
    def bounding_box(self, image_bytes, im_type, name):
        # Get the response text
        if im_type == "jpg":
            im_type = "jpeg"
        model = self.model_choices['box']
        model = self.models[model]
        prompt = """
        You will be given an image.
        If it is of a plane and the tail number (The unique number which identifies the plane) is *FULLY* visible in the image, return the bounding box of it. The box_2d should be [ymin, xmin, ymax, xmax] normalized to 0-1000. The box should fit as tightly to the tail number as possible.
        Otherwise, respond with just an empty list.
        """
        config = types.GenerateContentConfig(
            response_mime_type="application/json"
        )   
        response = self.client.models.generate_content(
            model=model,
            contents=[
                types.Part.from_bytes(
                data=image_bytes,
                mime_type='image/'+im_type,
                ),  
                prompt
            ],
            config = config
        )

        image = Image.open(io.BytesIO(image_bytes))
        width, height = image.size
        bounding_boxes = json.loads(response.text)
        print(response.text)
        if not bounding_boxes:
            print("No objects detected for", name)
            return 0
        
        if isinstance(bounding_boxes[0], int) == True:
            bounding_boxes = [{"box_2d":[bounding_boxes[0],bounding_boxes[1],bounding_boxes[2],bounding_boxes[3]]}]
        elif isinstance(bounding_boxes[0], dict) == False:
            bounding_boxes = [{"box_2d":[bounding_boxes[0][0],bounding_boxes[0][1],bounding_boxes[0][2],bounding_boxes[0][3]]}]


        for i, bounding_box in enumerate(bounding_boxes):
            print(i, bounding_box)
            abs_y1 = int(bounding_box["box_2d"][0] / 1000 * height)
            abs_y2 = int(bounding_box["box_2d"][2] / 1000 * height)
            box_height = abs(abs_y1 - abs_y2)
        if box_height < 20: # bounding box is 20px in height; not enough detail to read txt 
            return 1
        
        padding = 25 # make bounding box bigger to add resilience to mistakes 
        bounding_box["box_2d"][0] -= padding
        bounding_box["box_2d"][1] -= padding
        bounding_box["box_2d"][2] += padding
        bounding_box["box_2d"][3] += padding
        for i in range(4):
            if bounding_box["box_2d"][i] < 0:
                bounding_box["box_2d"][i] = 0
            if bounding_box["box_2d"][i] > 1000:
                bounding_box["box_2d"][i] = 1000
        
        image = self.get_im_with_box(image_bytes, name, response, [bounding_box])
        image.show()
        image.save(name.split(".")[0] + " with boxes" + "." + name.split(".")[1])
        return image

    def get_im_with_box(self, image_bytes, name, response, box):
        
        image = Image.open(io.BytesIO(image_bytes))
        width, height = image.size
        bounding_boxes = box
        print(response.text)
        if not bounding_boxes:
            print("No objects detected for", name)
            return    

        # Draw bounding boxes on image
        draw = ImageDraw.Draw(image)
        colors = ["red", "blue", "green", "yellow", "orange", "purple", "cyan"]

        for i, bounding_box in enumerate(bounding_boxes):
            print(i, bounding_box)
            abs_y1 = int(bounding_box["box_2d"][0] / 1000 * height)
            abs_x1 = int(bounding_box["box_2d"][1] / 1000 * width)
            abs_y2 = int(bounding_box["box_2d"][2] / 1000 * height)
            abs_x2 = int(bounding_box["box_2d"][3] / 1000 * width)

            color = colors[i % len(colors)]

            # Draw rectangle
            draw.rectangle([abs_x1, abs_y1, abs_x2, abs_y2], outline=color, width=1)

            # Draw label if available
            # label = bounding_box.get("label", f"Object {i+1}")
            # draw.text((abs_x1 + 4, abs_y1 + 4), label, fill=color)

        print("Image size:", width, height)
        print("Bounding boxes:", bounding_boxes)

        return image
    

comp = gemini_components()
# print(comp.request_gemini(image_bytes))
def test_acc(comp):
    answers = []
    with open("TestGem/answers/answers.txt", 'rb') as f:
        lines = f.readlines()

    # Each line as a list item (includes \n at end)
    for line in lines:
        answers.append(str(line.strip())[2:-1])  # .strip() removes the \n, the slicing removes artificats like b'
    print(answers)
    directory = os.fsencode("TestGem/Images")
    count = 0
    fails = [] 
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        with open("TestGem/Images/"+filename, 'rb') as f:
            if filename != "26.webp": # skip first 3 
                continue
            img_num, im_type = filename.split(".")
            img_num = int(img_num) - 1
            image_bytes = f.read()
            im_type = filename.split(".")[1]

            res = comp.request_gemini(image_bytes, im_type, filename)
            if "Error: " in res:
                res = res.split("Error: ")[1]
            print(res, " / ", answers[img_num], " / ", ("TestGem/Images/"+filename))
            if res != answers[img_num]:
                fails.append((res, answers[img_num], img_num))
                
            time.sleep(13) # 5 req /min cap
        count += 1
        print(len(fails)/count)
    print(fails)
    print(len(fails))
    print(len(fails)/count)

def test_vis(comp):
    answers = {}
    with open("TestGem/answers/answers.txt", 'rb') as f:
        lines = f.readlines()

    # Each line as a list item (includes \n at end)
    for idx, line in enumerate(lines):
        answers[idx] = str(line.strip())[2:-1]  # .strip() removes the \n + post processing other stuff
    
    

    print(answers)
    directory = os.fsencode("TestGem/Images")
    count = 0
    fails = [] 
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        with open("TestGem/Images/"+filename, 'rb') as f:
            img_num, im_type = filename.split(".")
            try:
                img_num = int(img_num) - 1
            except:
                img_num = img_num
            image_bytes = f.read()
            # image = Image.open(io.BytesIO(image_bytes))
            # image.show()
            im_type = filename.split(".")[1]
            res = comp.request_gemini(image_bytes, im_type, filename)
            if "Error: " in res:
                res = res.split("Error: ")[1]
            print(res, " / ", answers[img_num], " / ", ("TestGem/Images/"+filename))
            if res != answers[img_num]:
                fails.append((res, answers[img_num], img_num))
                
            time.sleep(2.5)
        count += 1
        print(len(fails)/count)
    print(fails)
    print(len(fails))


def test_box(comp):
    flag = True
    directory = os.fsencode("TestBox/Images")
    count = 0 
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        with open("TestBox/Images/"+filename, 'rb') as f:
            if "35" in filename:
                flag = False
                continue
            if flag:
                count += 1
                continue
            img_num, im_type = filename.split(".")
            try:
                img_num = int(img_num) - 1
            except:
                img_num = img_num
            image_bytes = f.read()
            # image = Image.open(io.BytesIO(image_bytes))
            # image.show()
            im_type = filename.split(".")[1]
            comp.bounding_box(image_bytes, im_type, filename)
            time.sleep(13)
        count += 1 

if __name__ == "__main__":
    test_acc(comp)
#21
#22
#31
#34
#35
#5

#18 points
#11/18 correct
# 4/4 obscured were detected as obscured
# correctly filtered 5/6 
# suitable for all phones past iphone 11

# model check: gemini-2.5-flash model extract: gemma-3-27b-it model box: gemini-2.5-flash
# ['N650GA', 'G-ZBJK', 'N236MJ', 'N61848', 'Tail Number Not Visible', 'Tail Number Not Visible', 'Tail Number Not Visible', 'Tail Number Not Visible', 'Tail Number Not Visible', 'EW-465TQ', 'F-M**O', 'Tail Number Not Visible', 'N955WN', 'Tail Number Not Visible', 'UR-82072', '29000', 'F-GSQU', 'Tail Number Not Visible', 'N225NE', 'Tail Number Not Visible', 'Tail Number Not Visible', 'Tail Number Not Visible', '3***', 'PH-BFV', 'TF-FIC', 'EW-465TQ', 'N4SD', 'N782SP', 'O*-59**5', 'N709PS', '124-100M', 'O-***', 'RA-*207*', 'Tail Number Not Visible']
# [
#   {"box_2d": [483, 608, 590, 755], "label": "tail number"}
# ]
# 0 {'box_2d': [483, 608, 590, 755], 'label': 'tail number'}
# [
#   {"box_2d": [483, 608, 590, 755], "label": "tail number"}
# ]
# 0 {'box_2d': [458, 583, 615, 780], 'label': 'tail number'}
# Image size: 655 318
# Bounding boxes: [{'box_2d': [458, 583, 615, 780], 'label': 'tail number'}]
# checked: <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=655x318 at 0x27379656210>
# N650GA  /  N650GA  /  TestGem/Images/1.jpg
# 0.0
# [
#   {"box_2d": [435, 252, 467, 321]}
# ]
# 0 {'box_2d': [435, 252, 467, 321]}
# [
#   {"box_2d": [435, 252, 467, 321]}
# ]
# 0 {'box_2d': [410, 227, 492, 346]}
# Image size: 1080 719
# Bounding boxes: [{'box_2d': [410, 227, 492, 346]}]
# checked: <PIL.WebPImagePlugin.WebPImageFile image mode=RGB size=1080x719 at 0x27379AAB610>
# EW-40570  /  EW-465TQ  /  TestGem/Images/10.webp
# 0.5
# [
#   {"box_2d": [604, 269, 656, 287], "label": "tail number"}
# ]
# 0 {'box_2d': [604, 269, 656, 287], 'label': 'tail number'}
# [
#   {"box_2d": [604, 269, 656, 287], "label": "tail number"}
# ]
# 0 {'box_2d': [579, 244, 681, 312], 'label': 'tail number'}
# Image size: 1080 719
# Bounding boxes: [{'box_2d': [579, 244, 681, 312], 'label': 'tail number'}]
# checked: <PIL.WebPImagePlugin.WebPImageFile image mode=RGB size=1080x719 at 0x273796565D0>
# Tail Number Not Visible  /  F-M**O  /  TestGem/Images/11.webp
# 0.6666666666666666
# [
#   [645, 570, 670, 625]
# ]
# 0 [645, 570, 670, 625]
# model check: gemini-2.5-flash model extract: gemma-3-27b-it model box: gemini-2.5-flash
# ['N650GA', 'G-ZBJK', 'N236MJ', 'N61848', 'Tail Number Not Visible', 'Tail Number Not Visible', 'Tail Number Not Visible', 'Tail Number Not Visible', 'Tail Number Not Visible', 'EW-465TQ', 'F-M**O', 'Tail Number Not Visible', 'N955WN', 'Tail Number Not Visible', 'UR-82072', '29000', 'F-GSQU', 'Tail Number Not Visible', 'N225NE', 'Tail Number Not Visible', 'Tail Number Not Visible', 'Tail Number Not Visible', '3***', 'PH-BFV', 'TF-FIC', 'EW-465TQ', 'N4SD', 'N782SP', 'O*-59**5', 'N709PS', '124-100M', 'O-***', 'RA-*207*', 'Tail Number Not Visible']
# [
#   {"box_2d": [566, 220, 586, 251], "label": "tail number"}
# ]
# 0 {'box_2d': [566, 220, 586, 251], 'label': 'tail number'}
# checked: 1
# Tail number too low quality  /  Tail Number Not Visible  /  TestGem/Images/12.webp
# 0.25
# [
#   {"box_2d": [471, 305, 508, 360, 566, 401]}
# ]
# 0 {'box_2d': [471, 305, 508, 360, 566, 401]}
# [
#   {"box_2d": [471, 305, 508, 360, 566, 401]}
# ]
# 0 {'box_2d': [446, 280, 533, 385, 566, 401]}
# Image size: 1080 720
# Bounding boxes: [{'box_2d': [446, 280, 533, 385, 566, 401]}]
# checked: <PIL.WebPImagePlugin.WebPImageFile image mode=RGB size=1080x720 at 0x2B581B08CD0>
# N827WN  /  N955WN  /  TestGem/Images/13.webp
# 0.4
# [
#   {
#     "box_2d": [
#       557,
#       250,
#       572,
#       296
#     ]
#   }
# ]
# 0 {'box_2d': [557, 250, 572, 296]}
# [
#   {
#     "box_2d": [
#       557,
#       250,
#       572,
#       296
#     ]
#   }
# ]
# 0 {'box_2d': [532, 225, 597, 321]}
# Image size: 1080 1440
# Bounding boxes: [{'box_2d': [532, 225, 597, 321]}]
# checked: <PIL.WebPImagePlugin.WebPImageFile image mode=RGB size=1080x1440 at 0x2B581B9C050>
# N789BA  /  Tail Number Not Visible  /  TestGem/Images/14.webp
# 0.5
# [
#   {"box_2d": [515, 621, 545, 715], "label": "tail number"}
# ]
# 0 {'box_2d': [515, 621, 545, 715], 'label': 'tail number'}
# [
#   {"box_2d": [515, 621, 545, 715], "label": "tail number"}
# ]
# 0 {'box_2d': [490, 596, 570, 740], 'label': 'tail number'}
# Image size: 1080 1440
# Bounding boxes: [{'box_2d': [490, 596, 570, 740], 'label': 'tail number'}]
# checked: <PIL.WebPImagePlugin.WebPImageFile image mode=RGB size=1080x1440 at 0x2B581B9DBA0>
# UR-82072  /  UR-82072  /  TestGem/Images/15.webp
# 0.42857142857142855
# [
#   495,
#   745,
#   525,
#   805
# ]
# ck: gemini-2.5-flash model extract: gemma-3-27b-it model box: gemini-2.5-flash
# ['N650GA', 'G-ZBJK', 'N236MJ', 'N61848', 'Tail Number Not Visible', 'Tail Number Not Visible', 'Tail Number Not Visible', 'Tail Number Not Visible', 'Tail Number Not Visible', 'EW-465TQ', 'F-M**O', 'Tail Number Not Visible', 'N955WN', 'Tail Number Not Visible', 'UR-82072', '29000', 'F-GSQU', 'Tail Number Not Visible', 'N225NE', 'Tail Number Not Visible', 'Tail Number Not Visible', 'Tail Number Not Visible', '3***', 'PH-BFV', 'TF-FIC', 'EW-465TQ', 'N4SD', 'N782SP', 'O*-59**5', 'N709PS', '124-100M', 'O-***', 'RA-*207*', 'Tail Number Not Visible']
# [
#   {"box_2d": [492, 693, 538, 725], "label": "tail number"}
# ]
# 0 {'box_2d': [492, 693, 538, 725], 'label': 'tail number'}
# [
#   {"box_2d": [492, 693, 538, 725], "label": "tail number"}
# ]
# 0 {'box_2d': [467, 668, 563, 750], 'label': 'tail number'}
# Image size: 1080 607
# Bounding boxes: [{'box_2d': [467, 668, 563, 750], 'label': 'tail number'}]
# checked: <PIL.WebPImagePlugin.WebPImageFile image mode=RGB size=1080x607 at 0x1CE78C747D0>
# 28000  /  29000  /  TestGem/Images/16.webp
# 0.125
# [
#   {
#     "box_2d": [409, 478, 425, 598]
#   }
# ]
# 0 {'box_2d': [409, 478, 425, 598]}
# checked: 1
# Tail number too low quality  /  F-GSQU  /  TestGem/Images/17.webp
# 0.2222222222222222
# [
#   {
#     "box_2d": [563, 615, 597, 703],
#     "label": "tail number"
#   }
# ]
# 0 {'box_2d': [563, 615, 597, 703], 'label': 'tail number'}
# [
#   {
#     "box_2d": [563, 615, 597, 703],
#     "label": "tail number"
#   }
# ]
# 0 {'box_2d': [538, 590, 622, 728], 'label': 'tail number'}
# Image size: 1080 682
# Bounding boxes: [{'box_2d': [538, 590, 622, 728], 'label': 'tail number'}]
# checked: <PIL.WebPImagePlugin.WebPImageFile image mode=RGB size=1080x682 at 0x1CE78C77B10>
# Tail Number Not Visible  /  Tail Number Not Visible  /  TestGem/Images/18.webp
# 0.2
# [
#   {"box_2d": [486, 172, 501, 232]}
# ]
# 0 {'box_2d': [486, 172, 501, 232]}
# [
#   {"box_2d": [486, 172, 501, 232]}
# ]
# 0 {'box_2d': [461, 147, 526, 257]}
# Image size: 1080 1440
# Bounding boxes: [{'box_2d': [461, 147, 526, 257]}]
# checked: <PIL.WebPImagePlugin.WebPImageFile image mode=RGB size=1080x1440 at 0x1CE78C77D90>
# N926AE  /  N225NE  /  TestGem/Images/19.webp
# 0.2727272727272727
# [
#   {"box_2d": [784, 137, 820, 233], "label": "tail number"}
# ]
# 0 {'box_2d': [784, 137, 820, 233], 'label': 'tail number'}
# [
#   {"box_2d": [784, 137, 820, 233], "label": "tail number"}
# ]
# 0 {'box_2d': [759, 112, 845, 258], 'label': 'tail number'}
# Image size: 1024 684
# Bounding boxes: [{'box_2d': [759, 112, 845, 258], 'label': 'tail number'}]
# checked: <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=1024x684 at 0x1CE78C77D90>
# G-ZCJK  /  G-ZBJK  /  TestGem/Images/2.jpg
# 0.3333333333333333
# []
# No objects detected for 20.webp
# checked: 0
# Tail number not identifiable  /  Tail Number Not Visible  /  TestGem/Images/20.webp
# 0.38461538461538464
# []
# No objects detected for 21.webp
# checked: 0
# Tail number not identifiable  /  Tail Number Not Visible  /  TestGem/Images/21.webp
# 0.42857142857142855
# []
# No objects detected for 22.webp
# checked: 0
# Tail number not identifiable  /  Tail Number Not Visible  /  TestGem/Images/22.webp
# 0.4666666666666667
# []
# No objects detected for 23.webp
# checked: 0
# Tail number not identifiable  /  3***  /  TestGem/Images/23.webp
# 0.5
# [
#   {"box_2d": [125, 126, 310, 840], "label": "tail number"}
# ]
# 0 {'box_2d': [125, 126, 310, 840], 'label': 'tail number'}
# [
#   {"box_2d": [125, 126, 310, 840], "label": "tail number"}
# ]
# 0 {'box_2d': [100, 101, 335, 865], 'label': 'tail number'}
# Image size: 1080 1080
# Bounding boxes: [{'box_2d': [100, 101, 335, 865], 'label': 'tail number'}]
# checked: <PIL.WebPImagePlugin.WebPImageFile image mode=RGB size=1080x1080 at 0x1CE78C77C50>
# PH-BFV  /  PH-BFV  /  TestGem/Images/24.webp
# 0.47058823529411764
# [
#   {"box_2d": [489, 275, 526, 363], "label": "tail number"}
# ]
# 0 {'box_2d': [489, 275, 526, 363], 'label': 'tail number'}
# [
#   {"box_2d": [489, 275, 526, 363], "label": "tail number"}
# ]
# 0 {'box_2d': [464, 250, 551, 388], 'label': 'tail number'}
# Image size: 1080 675
# Bounding boxes: [{'box_2d': [464, 250, 551, 388], 'label': 'tail number'}]
# checked: <PIL.WebPImagePlugin.WebPImageFile image mode=RGB size=1080x675 at 0x1CE78C77B10>
# TF-FIC  /  TF-FIC  /  TestGem/Images/25.webp
# 0.4444444444444444