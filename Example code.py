import Gemini_API as ai_api

ai_api.connect_to_wifi()

while True:
    reply = ai_api.query(input("Ask Gemini: "))
    print(reply)
