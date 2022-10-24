# import os

# from sys import exec_prefix

# from urllib.parse import quote

# import pyttsx3

# import speech_recognition as sr

# def takeCommand():

#     r = sr.Recognizer()

#     with sr.Microphone() as source:

#         r.adjust_for_ambient_noise(source)

#         r.energy_threshold = 1000

#         print("Listening...")

#         audio = r.listen(source)

#     try:

#         print("Recognizing...")

#         query = r.recognize_google(audio, language='ru-RU')#en-in

#         print(f"You Said:{query}\n")

#     except Exception as e:

#         print("Say Again Please...")

#         return "None"

#     return query


# query = takeCommand().lower()

# print(query)

import json

with open("tablets.json",'r') as file:
	a = json.load(file)


print(a["analgesic"][0]["image"])