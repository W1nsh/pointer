import curses

import webbrowser

from src.utils.rgb1k import rgb_to_1krgb
from src.config.config_parser import ConfigParser, Config
from src.point_handler import PointHandler
from src.config.point import Color


class App:
	def __init__(self, config_path: str, config_encoding: str) -> None:
		self.config_parser = ConfigParser(config_path, config_encoding)
		self.configurate()
		self.github_link = self.config.github_link
		self.tick = self.config.tick
		self.del_tail = self.config.del_tail
		self.del_last_checkpoints = self.config.del_last_checkpoints


	def configurate(self) -> None:
		config_dict = self.config_parser.read()
		self.config = self.config_parser.parse(config_dict)
		self.point_handler = self._init_point_handler(self.config)
		self.pair_list = self._init_color_pairs(
			self.config.point.color,
			self.config.checkpoint.color
		)


	def main(self, screen: curses.window) -> None:
		stop = False
		cp_del = curses.color_pair(1)
		cp_point = curses.color_pair(self.pair_list[0])
		cp_checkpoint = curses.color_pair(self.pair_list[1])
		self.point_handler.generate_point()
		last_checkpoint_y = -1
		last_checkpoint_x = -1
		while not stop:	
			screen.timeout(self.tick)
			key = screen.getch()
			stop = self._key_handler(key, stop)
			if self.point_handler.pos_is_point():
				last_checkpoint_x = self.point_handler.checkpoint_x
				last_checkpoint_y = self.point_handler.checkpoint_y
				if self.del_last_checkpoints:
					screen.addch(
						last_checkpoint_y,
						last_checkpoint_x,
						curses.ACS_BLOCK,
						cp_del,
					)
				else:
					screen.addch(
						last_checkpoint_y,
						last_checkpoint_x,
						curses.ACS_BLOCK,
						cp_checkpoint
					)
				self.point_handler.generate_point()
			last_point_x = self.point_handler.point_x
			last_point_y = self.point_handler.point_y
			if self.del_tail:
				if last_point_x != last_checkpoint_x or last_point_y != last_checkpoint_y:
					screen.addch(
						last_point_y,
						last_point_x,
						curses.ACS_BLOCK,
						cp_del,
					)
			self.point_handler.step_to_point()
			point_x = self.point_handler.point_x
			point_y = self.point_handler.point_y
			screen.addch(
				point_y,
				point_x,
				curses.ACS_BLOCK,
				cp_point,
			)
			checkpoint_x = self.point_handler.checkpoint_x
			checkpoint_y = self.point_handler.checkpoint_y
			screen.addch(
				checkpoint_y,
				checkpoint_x,
				curses.ACS_BLOCK,
				cp_checkpoint
			)
			screen.refresh()

	
	def _init_point_handler(self, config: Config) -> PointHandler:
		point_handler = PointHandler(
			config.point.position.x,
			config.point.position.y,
			config.checkpoint.border.x,
			config.checkpoint.border.y,
			config.checkpoint.indent.x,
			config.checkpoint.indent.y,
		)
		return point_handler
	

	def _init_color_pairs(self, *args: Color) -> list[int]:
		pair_list = []
		curses.init_pair(
			1,
			curses.COLOR_BLACK,
			curses.COLOR_BLACK,
		)
		for i, color in enumerate(args):
			color_1k = rgb_to_1krgb(
				color.r,
				color.g,
				color.b,
			)
			curses.init_color(
				i + 10,
				color_1k['r'],
				color_1k['g'],
				color_1k['b'],
			)
			curses.init_pair(
				i + 9,
				i + 10,
				curses.COLOR_BLACK,
			)
			pair_list.append(i + 9)
		return pair_list


	def _key_handler(self, ascii: int, stop: bool) -> bool:
		if ascii == 17:
			stop = True
		elif ascii == 23:
			webbrowser.open(self.github_link)
		return stop
