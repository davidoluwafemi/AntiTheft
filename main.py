from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from plyer import accelerometer
from kivy.factory import Factory
from kivy.uix.popup import Popup
from kivymd.toast import toast

def set_trigger_parameters(params):
	val = [params[0] + 0.8, params[0] - 0.8,
				params[1] + 0.8, params[1] - 0.8,
				params[2] + 0.8, params[2] - 0.8]
	return val
	
def smart_compare(val, var):
	if var[0] > val[0] or var[0] < val[1] or var[1] > val[2] or var[1] < val[3] or var[2] > val[4] or var[2] < val[5]:
		return True
	else:
		return False
            
Builder.load_string(''' 	
#:import MDDropdownMenu kivymd.uix.menu.MDDropdownMenu

<Arm>:
	ScreenManager:
		id: screens
		Screen:
			name: 'intro'
			FloatLayout:
				Label:
					canvas.before:
						Color:
							rgb: 0,0,0
						Rectangle:
							size: self.size
							pos: self.pos
				MDToolbar:
					title: app.title
					pos_hint: {"top": 1}
					md_bg_color: 0.545, 0, 0, 1
					background_palette: "Primary"
					elevation: 10
					right_action_items:
						[["dots-vertical", lambda x: MDDropdownMenu(items=app.menu_items, width_mult=3).open(self)]]
				Image:
					id: gif
					source: 'test1.gif'
					allow_stretch: True
					color: 1,0,0,1
					anim_delay: 0.001
					size_hint: 1, 1
					pos_hint: {'center_x': 0.5,"center_y":0.5}
				BoxLayout:
					id: arm_page
					size_hint: 1,0.5
					pos_hint: {'center_x': 0.5,"center_y":0.5}
					Button:
						id: arm_btn
						text: '[b][color=8b0000]Arm'
						markup: True
						font_size: dp(40)
						background_color: 0,0,0,0
						on_release: root.arm()
				Label:
					id: countdown
					text: ''
					markup: True
					font_size: dp(30)
					size_hint: 1,0.5
					pos_hint: {'center_x': 0.5,"center_y":0.5}
					
		Screen:
			name: 'trigger'
			FloatLayout:
				canvas.before:
					Color:
						rgb: 0,0,0
					Rectangle:
						size: self.size
						pos: self.pos
				Label:
					id: blink_text
					size_hint: 0.3,0.05
					pos_hint: {'center_x': 0.2,"center_y":0.96}
					text: ' '
					markup: True
					font_size: 25
					
<AboutMe@Popup>
	title: 'About'
	title_color: 1,1,1,1
	title_align: 'center'
	title_size: dp(20)
	auto_dismiss: False
	size_hint: 1,1
	background: 'popupbg.png'
	separator_color: 0,0,0,1
	FloatLayout:
		BoxLayout:
			size_hint: .8, .8
			pos_hint: {'center_x': .5, 'center_y': .58}
			canvas.before:
				Color:
					rgb: 0.545, 0, 0
				RoundedRectangle:
					size: self.size
					pos: self.pos
					radius: dp(10), dp(10), dp(10), dp(10)
		MDRaisedButton:
			text: 'Done'
			pos_hint: {'center_x': .5, 'center_y': .1}
			elevation_normal: 2
			opposite_colors: True
			md_bg_color: 0.545, 0, 0, 1
			on_release:  root.dismiss()
''')

class Arm(FloatLayout):
	
	def __init__(self, **kwargs):
		super(Arm,self).__init__(**kwargs)
		self.present_count = 5
		self.initial_axis = 0
		self.state = 0
	
	def arm(self):
		self.ids.arm_page.remove_widget(self.ids.arm_btn)
		Clock.schedule_interval(self.countdown, 1.1)
		
	def countdown(self, _):
		if not self.present_count:
			Clock.schedule_interval(self.theft_snifer, 1/20)
			Clock.unschedule(self.countdown)
			accelerometer.enable()
			self.ids.screens.current = 'trigger'
			toast('Anitheft mode active')
			
		elif self.present_count < 3:
			self.ids.countdown.text = '[b][color=ff0000]' + str(self.present_count)
			self.present_count -= 1
		else:
			self.ids.countdown.text = '[b]' + str(self.present_count)
			self.present_count -= 1
		
	def theft_snifer(self, _):
		val = accelerometer.acceleration[:3]
		
		if not val == (None, None, None):
			if not self.initial_axis:
				self.initial_axis = set_trigger_parameters(val)
			else:
				theft_status = smart_compare(self.initial_axis, val)
				if theft_status:
					Clock.unschedule(self.theft_snifer)
					self.alarm_owner()
				
					
	def alarm_owner(self):
		sound = SoundLoader.load('alert.wav')
		sound.play()



class Antitheft(MDApp):
	
	def __init__(self, **kwargs):
		self.title = "Antitheft"
		self.theme_cls.primary_palette = "Red"
		super().__init__(**kwargs)
		
	def build(self):
		self.menu_items = [{"viewclass": "MDMenuItem",
		"text": "About",
		"callback": self.callback_for_menu_items,}]
		self.root = Factory.Arm()
		
	def callback_for_menu_items(self, *args):
		Factory.AboutMe().open()
		
Antitheft().run()
        
