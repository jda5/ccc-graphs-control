from kivy.clock import Clock
from kivy.uix.screenmanager import Screen, ScreenManager
from widgets import COORDINATES, IDPopup


class Manager(ScreenManager):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.question_num = 0
		self.add_widget(HomeScreen(name=f"home_screen"))
		self.current = "home_screen"	

		for i in range(len(COORDINATES)):
			self.add_widget(TaskScreen(name=f"question_{i}"))


class HomeScreen(Screen):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.show_popup = True
		self.id_popup = IDPopup()

	def on_enter(self, *args):
		if self.show_popup:
			Clock.schedule_once(lambda dt: self.id_popup.open())
			self.show_popup = False


class TaskScreen(Screen):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.blank = True

	def on_enter(self):
		canvas = self.ids.get('canvas_widget', None)

		if canvas and self.blank:
			canvas.draw()
			self.blank = False

	def on_pre_enter(self):
		navigation = self.ids.get('navigation', None)
		if navigation:
			navigation.update_question_text()
			navigation.question_num = str(self.manager.question_num + 1)


class TutorialScreen(Screen):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.blank = True

	def on_enter(self):
		canvas = self.ids.get('canvas_widget', None)

		if canvas and self.blank:
			canvas.draw()
			self.blank = False
