import http.client
import json
import os
from config import target_lang
from dotenv import load_dotenv

def deeptrans(text):
    load_dotenv()

    conn = http.client.HTTPSConnection("deep-translate1.p.rapidapi.com")
    payload_j = {
        "q": text,
        "source": "en",
        "target": target_lang
    }   #json object is a dictionary

    payload = json.dumps(payload_j)    #converts the json object into string   

    headers = {
        'content-type': "application/json",
        'X-RapidAPI-Key': os.getenv("DEEPTR_RAPID_API"),
        'X-RapidAPI-Host': "deep-translate1.p.rapidapi.com"
    }
    
    conn.request("POST", "/language/translate/v2", payload, headers)

    res = conn.getresponse()
    data = res.read()
    
    try:
        return json.loads(data.decode("utf-8"))["data"]["translations"]["translatedText"]
    except KeyError:
        return "Please check your deepTranslate api key at .env file"