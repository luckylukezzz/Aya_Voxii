import http.client
import json

conn = http.client.HTTPSConnection("deep-translate1.p.rapidapi.com")

payload = "{\r\n    \"q\": \"lets play together\",\r\n    \"source\": \"en\",\r\n    \"target\": \"ja\"\r\n}"

headers = {
    'content-type': "application/json",
    'X-RapidAPI-Key': "be8ccbb9e0msh5115a6033bee5b6p105708jsn81d7946d1afe",
    'X-RapidAPI-Host': "deep-translate1.p.rapidapi.com"
}

conn.request("POST", "/language/translate/v2", payload, headers)

res = conn.getresponse()
data = res.read()


print("res type ",type(res))
print("data type " ,type(data))
print(json.loads(data.decode("utf-8"))["data"]["translations"]["translatedText"])

