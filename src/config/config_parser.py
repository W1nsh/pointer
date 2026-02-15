import json

from src.config.config import Config, Point
from src.config.point import Color, Position


class ConfigParser:
	def __init__(self, path: str, encoding: str) -> None:
		self.path = path
		self.encoding = encoding


	def read(self) -> dict[str, dict[str, dict[str, int | dict[str, int]]]]:
		with open(self.path, 'r', encoding=self.encoding) as f:
			config = json.load(f)
		return config


	def parse(self, config: dict) -> Config:
		cp = config['checkpoint']
		cp_b = cp['border']
		cp_b_x = cp_b['x']
		cp_b_y = cp_b['y']
		cp_i = cp['indent']
		cp_i_x = cp_i['x']
		cp_i_y = cp_i['y']
		cp_c = cp['color']
		cp_c_r = cp_c['r']
		cp_c_g = cp_c['g']
		cp_c_b = cp_c['b']
		cp_del_last = cp['del_last']
		checkpoint_color = Color(cp_c_r, cp_c_g, cp_c_b)
		checkpoint_indent = Position(cp_i_x, cp_i_y)
		checkpoint_border = Position(cp_b_x, cp_b_y)
		checkpoint = Point(
			color=checkpoint_color,
			indent=checkpoint_indent,
			border=checkpoint_border,
		)
		p = config['point']
		p_x = p['x']
		p_y = p['y']
		p_c = p['color']
		p_c_r = p_c['r']
		p_c_g = p_c['g']
		p_c_b = p_c['b']
		p_del_tail = p['del_tail']
		point_color = Color(p_c_r, p_c_g, p_c_b)
		point_position = Position(p_x, p_y)
		point = Point(
			color=point_color,
			position=point_position,
		)
		github_link = config['github_link']
		tick = config['tick']
		config_obj = Config(checkpoint, point, github_link, tick, p_del_tail, cp_del_last)
		return config_obj
	