# kivy app imports
from kivymd.app import MDApp
from kivy.app import App
from kivy.factory import Factory

# layout imports
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup

# kivy clock import
from kivy.clock import Clock

# kivy sound player import
from kivy.core.audio import SoundLoader

# android accelerometer hardware import
from plyer import accelerometer

# threshold value generator import
import set_threshold

# trigger bool import
from compare import trigger_bool


# tilt sensivity value
sensivity = 0.7


class Arm(FloatLayout):
	
	def __init__(self, **kwargs):
		super(Arm,self).__init__(**kwargs)
		self.present_count = 5
		self.initial_axis = 0
		self.state = 0
	
	# event button that start countdown down to arm device
	def arm(self):
		self.ids.arm_page.remove_widget(self.ids.arm_btn)
		Clock.schedule_interval(self.countdown, 1.1)
		
	# this is a method that vounts doen to arm device
	# and unschedule the clock class that is handling this
	# method and starts the interval to snift theft
	def countdown(self, _):
		
		if not self.present_count:
			Clock.schedule_interval(self.theft_snifer, 1/20)
			Clock.unschedule(self.countdown)
			accelerometer.enable()
			self.ids.screens.current = 'trigger'
			
		elif self.present_count < 3:
			self.ids.countdown.text = '[b][color=ff0000]' +\
				str(self.present_count)
			self.present_count -= 1
			
		else:
			self.ids.countdown.text = '[b]' +\
				 str(self.present_count)
			self.present_count -= 1
		
	def theft_snifer(self, _):
		# generates new accelerometer sensor reading
		new_val = accelerometer.acceleration[:3]
		
		if not new_val == (None, None, None):
			if not self.initial_axis:
				self.initial_axis = set_threshold.value(new_val, sensivity)
				
			else:
				# compares whether new value is in range of threshold
				theft_status = trigger_bool(
					self.initial_axis,
					new_val
				)
				
				# this sounds the siren alarm
				if theft_status:
					Clock.unschedule(self.theft_snifer)
					self.alarm_owner()
				
	# plays siren sound			
	def alarm_owner(self):
		sound = SoundLoader.load('alert.wav')
		sound.play()



class AntitheftApp(MDApp):
	
	def __init__(self, **kwargs):
		self.title = "Antitheft"
		self.theme_cls.primary_palette = "Red"
		super().__init__(**kwargs)
		
	def build(self):
		self.menu_items = [
			{
				"viewclass": "MDMenuItem",
				"text": "About",
				"callback": self.callback_for_menu_items,
			}
		]
		self.root = Factory.Arm()
		
	def callback_for_menu_items(self, *args):
		Factory.AboutMe().open()
		
AntitheftApp().run()