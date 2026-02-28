from google import genai
from google.genai import types
from keys import keyStore
import os
import time
# Configure the API key





class gemini_components():
    def __init__(self):
        store = keyStore() 
        store.add_gemini_key()
        gemini_key = store.keys["gemini"]

        self.client = genai.Client(api_key = gemini_key)
        self.prompt = """
        You will be given an image. 
        Determine based *ONLY* on the contents of the image and no external information if: 1) there is a plane in the image, 2) if the tail number is visible, and 3) what the tail number is. Then, respond according to the following rules:
            If there is no plane in the photo:
                'Error: No Plane'
            If the tail number isnt shown in the image or if the image is too low quality to read the tail number:
                'Error: Tail Number Not Visible'
            if tail number is partially obscured / the image quality is not good enough to make out some digits:
                'Tail number: <Tail number with obscured/low confidence characters replaced with '*', e.g. G-*LM*P>'
            If and only if tail number *fully* visible:
                'Tail number: <Tail number, e.g. G-HLMOP>'
        You should respond in exactly this format, with no other text.
        """
        self.models = ["gemini-2.5-flash", "gemma-3-27b-it", "gemma-3-12b-it", "gemini-3-flash-preview", "gemini-2.5-flash-lite"]
        self.model_choices = {"check":1, "extract":1}
        print("model check:",self.models[self.model_choices['check']],"model extract:",self.models[self.model_choices['extract']])

    def request_gemini(self, image_bytes, im_type):
        if im_type == "jpg":
            im_type = "jpeg"
        vis = self.check_vis(image_bytes, im_type)
        print("checked:", vis)
        if "Error" in vis:
            return vis
        
        time.sleep(2.5)
        tail = self.request_gemini_extract(image_bytes, im_type)
        
        if "Tail number: " in tail:
            tail = tail.split("Tail number: ")[1]
        return tail
    

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
        
    def request_gemini_extract(self, image_bytes, im_type):
        # Get the response text
        model = self.model_choices['extract']
        model = self.models[model]
        response = self.client.models.generate_content(
            model=model,
            contents=[
                types.Part.from_bytes(
                data=image_bytes,
                mime_type='image/'+im_type,
                ),
                self.prompt
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