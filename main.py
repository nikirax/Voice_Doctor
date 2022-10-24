from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window
import webbrowser
from gtts import gTTS
from playsound import playsound 
from os import remove
import pyaudio
import wave
from kivy.uix.screenmanager import ScreenManager, Screen
import wavio as wv
from kivy.uix.image import AsyncImage
import speech_recognition as sr 
import json

#Window.size = (520, 1080)
with open("voice.kv", 'r') as file:
	KV = file.read()

class MainApp(MDApp):
	def build(self):
		self.theme_cls.theme_style_switch_animation = True
		self.theme_cls.theme_style = "Dark"
		self.theme_cls.material_style = "M3"
		return Builder.load_string(KV)
	def switch_main_theme(self):
		self.theme_cls.theme_style = ("Dark" if self.theme_cls.theme_style == "Light" else "Light")
	def switch_micro_style(self):
		self.root.ids.btn.icon = "assets/micro_red.png"
		#playsound("C:\\Users\\User\\Desktop\\шняга\\python_test\\voice_doc\\assets\\assistent.mp3")
		Clock.schedule_once(self.Recognize_Stream_Audio, 0.0001)
	def Recognize_Stream_Audio(self, dt):
		filename = "assets/record.wav"
		self.Stream_Microphone(filename)
		self.root.ids.btn.icon = "assets/micro.png"
		self.Recognize_Audio(filename)
	def Stream_Microphone(self, filename):
		chunk = 1024
		FORMAT = pyaudio.paInt16
		channels = 1
		sample_rate = 44100
		record_seconds = 5
		p = pyaudio.PyAudio()
		stream = p.open(format=FORMAT,
						channels=channels,
						rate=sample_rate,
						input=True,
						output=True,
						frames_per_buffer=chunk)
		frames = []
		for i in range(int(44100 / chunk * record_seconds)):
			data = stream.read(chunk)
			frames.append(data)
		stream.stop_stream()
		stream.close()
		p.terminate()
		wf = wave.open(filename, "wb")
		wf.setnchannels(channels)
		wf.setsampwidth(p.get_sample_size(FORMAT))
		wf.setframerate(sample_rate)
		wf.writeframes(b"".join(frames))
		wf.close()
	def Recognize_Audio(self, filename):
		# r = sr.Recognizer()
		# text = ""
		# with sr.AudioFile(filename) as source:
		# 	audio_data = r.record(source)
		# 	text = r.recognize_google(audio_data)
		# remove(filename) 
		# if text == "hello" or text == "Hello":
		# 	self.Open_Tablets() 
		# 	mytext = 'Привет я ассистент Аня, вот что я вам подобрала'
		# 	language = 'ru'
		# 	myobj = gTTS(text=mytext, lang=language, slow=False)
		# 	path_voice = "assets/assistent.mp3"
		# 	playsound("assets/assistent.mp3")
		# 	myobj.save(path_voice)
		self.Open_Tablets()
	def Open_Tablets(self):
		with open("tablets.json",'r') as file:
			a = json.load(file)
		self.root.current = "carousel"
		for i in range(0,2):
			self.root.ids[f"label_{i+1}_"].text = a["analgesic"][i]["recomendation_en"]
			self.root.ids[f"label_{i+1}"].text = a["analgesic"][i]["name_en"] 
			self.root.ids[f"image_{i+1}"].source = a["analgesic"][i]["image"]
	def Back_Main(self):
		self.root.current = "main"

	def on_chevron(self):
		settings_card_items = [self.root.ids.volume_slider,self.root.ids.volume_value,self.root.ids.volume,self.root.ids.switch_language]
		card = self.root.ids.settings_card
		if card.card_open == False:
			card.size_hint = [0.001, 0.001]
			card.pos_hint = {"center_x": 1, "center_y": 1}
			for item in settings_card_items:
				item.opacity = 1
			self.root.ids.volume_slider.disabled = False
			Clock.schedule_interval(self.open_settings_card, 0.0001)
		else:
			Clock.schedule_interval(self.close_settings_card, 0.0001)
	def open_settings_card(self, dt):
		card = self.root.ids.settings_card
		if card.size_hint[0] >= 0.7:
			card.card_open = True
			return False
		if card.size_hint[0] < 0.7:
			card.size_hint[0] += 0.01
		if card.size_hint[1] < 0.4:
			card.size_hint[1] += 0.01
		if card.pos_hint["center_x"] > 0.5:
			card.pos_hint["center_x"] -= 0.01
		if card.pos_hint["center_y"] > 0.5:
			card.pos_hint["center_y"] -= 0.01
		return True
	def close_settings_card(self, dt):
		settings_card_items = [self.root.ids.volume_slider,self.root.ids.volume_value,self.root.ids.volume,self.root.ids.switch_language]
		card = self.root.ids.settings_card
		if card.size_hint[0] <= 0.002:
			for item in settings_card_items:
				item.opacity = 0
			self.root.ids.volume_slider.disabled = True
			card.card_open = False
			return False
		if card.size_hint[0] > 0.002:
			for item in settings_card_items:
				if item.opacity != 0:
					item.opacity -= 0.02
			card.size_hint[0] -= 0.01
		if card.size_hint[1] > 0.002:
			card.size_hint[1] -= 0.01
	def open_video(self):
		webbrowser.open('https://t.me/hollosan', new=2)


MainApp().run()