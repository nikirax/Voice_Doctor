#create by https://github.com/nikirax
#create with fraimworks kivy and kivymd
#kivy: https://github.com/kivy/kivy
#kivymd: https://github.com/kivymd/KivyMD
 
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window
import webbrowser
from playsound import playsound 
from os import remove
import pyaudio
import wave
import speech_recognition as sr 
import json

#Regular application size
#Window.size = (520, 1080)

# open and read struct application
with open("voice.kv", 'r') as file:
	KV = file.read()

#main function
class MainApp(MDApp):

	#build start menu and style application
	def build(self):
		self.theme_cls.theme_style = "Dark"
		self.theme_cls.material_style = "M3"
		self.language = True
		return Builder.load_string(KV)

		#button in settingss switch_language
	def switch_language(self):
		self.language = not(self.language)

		#button in main menu switch dark and sun theme
	def switch_main_theme(self):
		self.theme_cls.theme_style = ("Dark" if self.theme_cls.theme_style == "Light" else "Light")

		#button in main menu micro
	def switch_micro_style(self):
		#TODO: make sure that the micro does not move out when pressed
		#self.root.ids.btn.icon = "assets/micro_red.png"
		#playsound("C:\\Users\\User\\Desktop\\шняга\\python_test\\voice_doc\\assets\\assistent.mp3")

		#asynchronous click call
		Clock.schedule_once(self.Recognize_Stream_Audio, 0.0001)

		# recognize file with voice
	def Recognize_Stream_Audio(self, dt):
		try:
			filename = "assets/record.wav"
			self.Stream_Microphone(filename)
			self.root.ids.btn.icon = "assets/micro.png"
			self.Recognize_Audio(filename)
		except:
			print("Error Not Text")

		# record your voice
	def Stream_Microphone(self, filename):
		try:
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
		except:
			print("Error Not Text")

		# recognize your voice
	def Recognize_Audio(self, filename):
		r = sr.Recognizer()
		text = ""

		if self.language == True:
			loc = "en-En"
		else:
			loc = "ru-Ru"
		
		#from voice to string
		with sr.AudioFile(filename) as source:
			audio_data = r.record(source)
			text = r.recognize_google(audio_data, language=loc)

		remove(filename) 
		print(text) 
		text = text.lower()

		#TODO: complete translation and recognition via json
		if text == "болит живот" or text == "stomach aches":
			self.Open_Tablets("analgesic")
			print(text) 
		elif text == "болит голова" or text == "my head":
			print(text)
			self.Open_Tablets("ForBelly")

		# load new screen with tablets
	def Open_Tablets(self, med):
		if self.language == True:
			loc = "en"
		else:
			loc = "ru"
		with open("tablets.json",'r', encoding="utf8") as file:
			a = json.load(file)
		self.root.current = "carousel"
		
		#TODO: complete carousel infinity
		for i in range(0,3):
			self.root.ids[f"label_{i+1}_"].text = a[med][i][f"recomendation_{loc}"]
			self.root.ids[f"label_{i+1}"].text = a[med][i][f"name_{loc}"] 
			self.root.ids[f"image_{i+1}"].source = a[med][i]["image"]
		
		#Button back in tablets screen
	def Back_Main(self):
		self.root.current = "main"

		#Open settings animated
	def on_chevron(self):
		settings_card_items = [self.root.ids.volume_slider,self.root.ids.volume_value,self.root.ids.volume,self.root.ids.switch_language,self.root.ids.docs]
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
		
		#Open settings animated
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

		#Close settings animated
	def close_settings_card(self, dt):
		settings_card_items = [self.root.ids.volume_slider,self.root.ids.volume_value,self.root.ids.volume,self.root.ids.switch_language,self.root.ids.docs]
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
		
		#Button in settings docs on this project
	def open_video(self):
		webbrowser.open('https://github.com/nikirax/Voice_Doctor', new=2)

#run main function
if __name__ == '__main__':
	MainApp().run()