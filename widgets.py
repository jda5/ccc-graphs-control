from kivy.graphics import Color, Line
from kivy.properties import BooleanProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget


COORDINATES = (
    (1, 5, 2, 7),
    (2, 11, 13, 22),
    (3, 4, 5, 20),
    (4, 13, 1, -5),
    (-3, 22, 1, 2),
    (3, -11, -2, 9),
    (5, 133, 2, 58),
    (-1, -4, 8, 23),
    (4, -17, -2, 31),
    (4, 11, -2, -13),
    (2, -16, -3, 19),
    (-8, -2, -4, -6),
    (-4, -40, -6, -62),
    (-1, -7, 19, 133),
    (14, 5, 6, 5),
    (77, -3, 41, -3),
    (2, 5, 10, 9),
    (3, -7, 27, 1),
    (-1, 1, 7, 5),
    (40, 10, 20, 5),
)


class NavigationPane(FloatLayout):

	def next(self):
		manager = self.parent.parent.manager
		if manager.question_num < len(COORDINATES) - 1:
			manager.question_num += 1
			manager.transition.direction = 'left'
			manager.current = f"question_{manager.question_num}"

	def previous(self):
		manager = self.parent.parent.manager
		if manager.question_num > 0:
			manager.question_num -= 1
			manager.transition.direction = 'right'
			manager.current = f"question_{manager.question_num}"

	def update_question_text(self):
		"""
		Changes the text of the label with id 'Question'.
		"""
		manager = self.parent.parent.manager
		x1, y1, x2, y2 = COORDINATES[manager.question_num]
		self.question_text = f"Find the equation of a line that goes through the coordinates ({x1}, {y1}) and ({x2}, {y2})"


class CanvasWidget(Widget):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.pen_color = [0, 0, 0, 1]
		self.pen_width = 2
		self.drawing = True

	def on_touch_down(self, touch):
		"""
		When touched the widget creates a data entry in the user data dictionary corresponding to the Touch object
		called 'current_line' whose value is a Line object of position touch.x and touch.y.
		:param touch: A Touch object - see https://kivy.org/doc/stable/guide/inputs.html#touch-events for more details
		"""
		# Begin drawing only if the touch falls inside the widget and writing is set to True and the user hasn't already
		# submitted an answer
		if self.collide_point(touch.x, touch.y):
			with self.canvas.before:
				Color(*self.pen_color)
				touch.ud['current_line'] = Line(
					points=(touch.x, touch.y), width=self.pen_width
				)
			if not self.drawing:
				self.eraser.center = touch.pos							# Move the drawing circle to the location of the touch
				self.eraser.visible = True								# Show the drawing circle

	def on_touch_move(self, touch):
		"""
		Uses the dict.get() method to returns the value for the 'current_line'. If 'current_line' is not None then
		points are added to the line corresponding to the touch's x and y coordinates.
		:param touch: A Touch object - see https://kivy.org/doc/stable/guide/inputs.html#touch-events for more details
		"""
		if self.collide_point(touch.x, touch.y):
			line = touch.ud.get('current_line')
			if line:
				line.points += (touch.x, touch.y)
			if not self.drawing:
				self.eraser.center = touch.pos  						# Move the drawing circle to the location of the touch

	def on_touch_up(self, touch):
		"""
		Sets allow_drawing to False
		:param touch: A Touch object - see https://kivy.org/doc/stable/guide/inputs.html#touch-events for more details
		"""
		if not self.drawing:
			self.eraser.visible = False  								# Hide the drawing circle

	def clear_canvas(self):
		self.canvas.after.clear()

	def switch_draw_mode(self, icon_button):
		"""
		This function switches between the pen and the eraser by increaseing the line width and changing the colour from black to white
		"""
		icon_button.pen_icon = not icon_button.pen_icon
		if self.drawing:
			self.pen_color = [1, 1, 1, 1]
			self.pen_width = self.eraser.width
		else:
			self.pen_color = [0, 0, 0, 1]
			self.pen_width = 2
		self.drawing = not self.drawing

	def draw(self, *args):
		grid_size = self.width / 14
		with self.canvas.after:
			Color(0.92, 0.92, 0.92, 0.5)
			for i in range(1, int(self.width // grid_size)):
				Line(points=[self.x + (grid_size * i), self.y, self.x + (grid_size * i), self.y + self.height],
					width=1, cap='square')
			for i in range(1, int(self.height // grid_size) + 1):
				Line(points=[self.x, self.y + (grid_size * i), self.x + self.width, self.y + (grid_size * i)],
					width=1, cap='square')


class RoundedButton(ButtonBehavior, Label):

    def on_disabled(self, *args):
        """
        Callback for when self.disabled is changed. If True then disabled reduce saturation and value by 11%, otherwise
        increase saturation and value by 11%.
        :param args: args inherited from callback - not needed
        """
        if self.disabled:
            self.color = [0.75, 0.75, 0.75, 1]
        else:
            self.color = [1, 1, 1, 1]


class IDInput(TextInput):

    def insert_text(self, substring, from_undo=False):
        if substring.isnumeric():
            if len(self.text) < 1:
                super().insert_text(substring, from_undo=from_undo)
                self.focus_next_input()

    def focus_next_input(self):
        self.focus = False
        if self.next_input is not None:
            self.next_input.focus = True


class IDPopup(Popup):
    
    def submit(self):
        user_id = ''
        for id_input in reversed(self.ids['id_boxlayout'].children):
            if id_input.text == '':
                id_input.focus = True
                return
            user_id += id_input.text
       	# TODO: Save ID number and make use of it
        self.close_popup()

    def close_popup(self):
        return super().dismiss()
