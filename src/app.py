import curses

import webbrowser
from pathlib import Path

from src.utils.rgb1k import rgb_to_1krgb
from src.config.config_parser import ConfigParser, Config
from src.point_handler import PointHandler
from src.config.point import Color


class App:
	def __init__(self, config_path: Path, config_encoding: str) -> None:
		self._path_exists(config_path)
		self.config_parser = ConfigParser(config_path, config_encoding)
		self._configure()
		self.github_link = self.config.github_link
		self.tick = self.config.tick
		self.del_tail = self.config.del_tail
		self.del_last_checkpoints = self.config.del_last_checkpoints


	def main(self, screen: curses.window) -> None:
		stop = False
		cp_del = curses.color_pair(self.pair_list[0])
		cp_point = curses.color_pair(self.pair_list[1])
		cp_checkpoint = curses.color_pair(self.pair_list[2])
		self.point_handler.generate_point()
		last_checkpoint_y = -1
		last_checkpoint_x = -1
		while not stop:	
			screen.timeout(self.tick)
			key = screen.getch()
			stop = self._key_handler(key, stop)
			if self.point_handler.point_is_checkpoint():
				last_checkpoint_x = self.point_handler.checkpoint_x
				last_checkpoint_y = self.point_handler.checkpoint_y
				if self._term_size_handler(
					last_checkpoint_x, 
					last_checkpoint_y, 
					curses.COLS, 
					curses.LINES,
					):
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
					if self._term_size_handler(
					last_point_x, 
					last_point_y, 
					curses.COLS, 
					curses.LINES,
					):
						screen.addch(
							last_point_y,
							last_point_x,
							curses.ACS_BLOCK,
							cp_del,
						)
			self.point_handler.step_to_point()
			point_x = self.point_handler.point_x
			point_y = self.point_handler.point_y
			if self._term_size_handler(
				point_x, 
				point_y, 
				curses.COLS, 
				curses.LINES,
				):
				screen.addch(
					point_y,
					point_x,
					curses.ACS_BLOCK,
					cp_point,
				)
			checkpoint_x = self.point_handler.checkpoint_x
			checkpoint_y = self.point_handler.checkpoint_y
			if self._term_size_handler(
				checkpoint_x, 
				checkpoint_y, 
				curses.COLS, 
				curses.LINES,
				):
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
		for i, color in enumerate(args):
			color_1k = rgb_to_1krgb(
				color.r,
				color.g,
				color.b,
			)
			curses.init_color(
				i,
				color_1k['r'],
				color_1k['g'],
				color_1k['b'],
			)
			curses.init_pair(
				i + 9,
				i,
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


	def _path_exists(self, path: Path) -> None:
		if not path.exists():
			raise RuntimeError(f'Config file with path {path} not found')


	def _configure(self) -> None:
		self.config = self.config_parser.parse()
		self.point_handler = self._init_point_handler(self.config)
		self.pair_list = self._init_color_pairs(
			self.config.background_color,
			self.config.point.color,
			self.config.checkpoint.color,
		)

	
	def _xy_in_range(
			self,
			x: int,
			y: int,
			cols: int,
			lines: int,
	) -> bool:
		return (x in range(0, cols) and (y in range(0, lines)))


	def _term_size_handler(self, x: int, y: int, cols: int, lines: int) -> bool | None:
		if self._xy_in_range(x, y, cols, lines):
			return True
		else:
			raise RuntimeError('''
				The terminal is smaller in size 
				than the values specified in the config'
			''')
