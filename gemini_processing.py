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
        self.model_choices = {"check":0, "extract":1, "box":0}
        print("model check:",self.models[self.model_choices['check']],"model extract:",self.models[self.model_choices['extract']])

    def request_gemini(self, image_bytes, im_type):
        if im_type == "jpg":
            im_type = "jpeg"
        first_answer =  self.bounding_box(image_bytes, im_type)
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
        
        time.sleep(2.5)
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
        

        for i, bounding_box in enumerate(bounding_boxes):
            print(i, bounding_box)
            abs_y1 = int(bounding_box["box_2d"][0] / 1000 * height)
            abs_y2 = int(bounding_box["box_2d"][2] / 1000 * height)
            height = abs(abs_y1 - abs_y2)
        if height < 20:
            return 1
        
        padding = 25 
        bounding_box[0] -= padding
        bounding_box[1] -= padding
        bounding_box[2] += padding
        bounding_box[3] += padding
        image = self.get_im_with_box(image_bytes, name, response, [bounding_box])
        image.save(name.split(".")[0] + " with boxes" + "." + name.split(".")[1])
        return image

    def get_im_with_box(self, image_bytes, name, response, box):
        
        image = Image.open(io.BytesIO(image_bytes))
        width, height = image.size
        bounding_boxes = json.loads(response.text)
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
            draw.rectangle([abs_x1, abs_y1, abs_x2, abs_y2], outline=color, width=3)

            # Draw label if available
            label = bounding_box.get("label", f"Object {i+1}")
            draw.text((abs_x1 + 4, abs_y1 + 4), label, fill=color)

        print("Image size:", width, height)
        print("Bounding boxes:", bounding_boxes)

        return image
    
    
    def check_vis(self, image_bytes, im_type):
        # Get the response text
        model = self.model_choices['check']
        model = self.models[model]
        prompt = """
        You will be given an image. 
        Determine based *ONLY* on the contents of the image and no external information if: 1) there is a plane in the image, and 2) if the tail number is readable from the image (e.g. if the image is high enough quality to read it, it isn't obscured in the image etc../). Then, respond according to the following rules:
            If there is no plane in the photo:
                'Error: No Plane'
            If the tail number can't be read accurately (either due to obstruction or low quality):
                'Error: Cant get tail number'
            Otherwise (if the tail number is readable):
                'Good Image'
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
# # Load an image
# image = Image.open("Test_tail.jpg")
# with open('Test_tail.jpg', 'rb') as f:
#     image_bytes = f.read()

comp = gemini_components()
# print(comp.request_gemini(image_bytes))
def test_acc(comp):
    answers = []
    with open("TestGem/answers/answers.txt", 'rb') as f:
        lines = f.readlines()

    # Each line as a list item (includes \n at end)
    for line in lines:
        answers.append(str(line.strip())[2:-1])  # .strip() removes the \n
    print(answers)
    directory = os.fsencode("TestGem/Images")
    count = 0
    fails = [] 
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        with open("TestGem/Images/"+filename, 'rb') as f:
            img_num, im_type = filename.split(".")
            img_num = int(img_num) - 1
            image_bytes = f.read()
            # image = Image.open(io.BytesIO(image_bytes))
            # image.show()
            im_type = filename.split(".")[1]
            res = comp.request_gemini(image_bytes, im_type)
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
            res = comp.request_gemini(image_bytes, im_type)
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

test_box(comp)
#21
#22
#31
#34
#35
#5
