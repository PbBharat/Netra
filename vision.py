import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/aneesh.paul/Downloads/team-medy-buddy-aa4016a467d2.json"

import json

from PIL import Image as PIL_Image
from PIL import ImageOps as PIL_ImageOps

from datetime import datetime

from direct_data import data_import



# Define project information
PROJECT_ID = "team-medy-buddy"  # @param {type:"string"}
LOCATION = "us-central1"  # @param {type:"string"}


import vertexai
from vertexai import generative_models
# from vertexai.generative_models import GenerationConfig, GenerativeModel, Image, Part


def find_first_and_last_curly_brackets(s):
    first = s.find('{')
    last = s.rfind('}')
    
    if first == -1 or last == -1:
        return "Curly brackets not found."
    else:
        return s[first:last+1]
    

def month_difference(date_string):
    # Convert the input string to a datetime object, assuming day as 1
    input_date = datetime.strptime(date_string, "%m/%Y")
    
    # Get the current date
    current_date = datetime.now()
    
    # Calculate the difference in months
    month_diff = (current_date.year - input_date.year) * 12 + current_date.month - input_date.month
    
    return 0 - month_diff



def generate_text(image_path: str) -> str:

    image = generative_models.Image.from_bytes(image_path)


    # Initialize Vertex AI
    vertexai.init(project=PROJECT_ID, location=LOCATION)

    # Load the model
    model = generative_models.GenerativeModel("gemini-1.0-pro-vision")

    # Generation config
    config = {"max_output_tokens": 2048, "temperature": 0.4, "top_p": 1, "top_k": 32}

    # Safety config
    safety_config = {
        generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
        generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
        generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
        generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
        generative_models.HarmCategory.HARM_CATEGORY_UNSPECIFIED: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    }


    prompt= """You will given an image of the backside of a tablet strip. At first step, you have to read the text on that image.
    Finally, Your task is to extract key pisces of information from the text read by you. You have to give the information in a json format. If any information is not available, mention "Not provided".
    Expected Output and List of key information:
    {"medicine_name": <Name of the medicine>,
    "mfg_month" : < Manufacturing Month and Year of the medicine in strictly in "MM/YYYY" format >,
    "exp_month" : < Expiry or exp Month and Year of the medicine in "MM/YYYY" format >}
    Only give json in your outout."""



    # Generate content
    responses = model.generate_content(
        [image, prompt],
        generation_config=config,
        # stream=True,
        safety_settings=safety_config,
    )
    
    try:

        ans_json_str= find_first_and_last_curly_brackets(responses.text)
        ans_dic= json.loads(ans_json_str)

        exp_month_string = ans_dic["exp_month"]

        exp_diff= month_difference(exp_month_string)

        if exp_diff <0:
            voice= "इस दवा की एक्सपायरी डेट खत्म हो चुकी है"
        elif exp_diff >0:
            voice= f"इस दवा की एक्सपायरी डेट {exp_diff} महीने में खत्म हो जाएगी."
        elif exp_diff ==0:
            voice= "इस दवा की एक्सपायरी डेट इसी महीने होगी."

        ans_dic.update({"voice" : voice})

        try:
            medicine_name= ans_dic.get("medicine_name")
            data_drug= data_import(medicine_name)
            ans_dic.update(data_drug)


        except:
            pass

        return ans_dic


        return responses.text
    except:
        return "Error in OCR"
