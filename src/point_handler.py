import random


class PointHandler:
	def __init__(
			self,
			point_x: int,
			point_y: int,
			border_x: int,
			border_y: int,
			border_indent_x: int,
			border_indent_y: int,
	) -> None:
		self.point_x = point_x
		self.point_y = point_y
		self.border_x = border_x
		self.border_y = border_y
		self.border_indent_x = border_indent_x
		self.border_indent_y = border_indent_y

	
	def step_to_point(self) -> None:
		if self.point_x < self.checkpoint_x:
			self.point_x += 1
		elif self.point_x > self.checkpoint_x:
			self.point_x -= 1
		if self.point_y < self.checkpoint_y:
			self.point_y += 1
		elif self.point_y > self.checkpoint_y:
			self.point_y -= 1

	
	def generate_point(self) -> None:
		self.checkpoint_x = random.randint(self.border_indent_x, self.border_x - self.border_indent_x)
		self.checkpoint_y = random.randint(self.border_indent_y, self.border_y - self.border_indent_y)


	def pos_is_point(self) -> bool:
		return self.point_x == self.checkpoint_x and self.point_y == self.checkpoint_y
