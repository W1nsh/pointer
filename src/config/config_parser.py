import json
from pathlib import Path

from src.config.config import Config, Point
from src.config.point import Color, Position


class ConfigParser:
	def __init__(self, config_path: Path, encoding: str) -> None:
		self.config_path = config_path
		self.encoding = encoding


	def parse(self) -> Config:
		config_content = self.config_path.read_text(encoding=self.encoding)
		config = json.loads(config_content)
		cp = config['checkpoint']
		cp_b_x = cp['border']['x']
		cp_b_y = cp['border']['y']
		cp_i_x = cp['indent']['x']
		cp_i_y = cp['indent']['y']
		cp_c_r = cp['color']['r']
		cp_c_g = cp['color']['g']
		cp_c_b = cp['color']['b']
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
		p_c_r = p['color']['r']
		p_c_g = p['color']['g']
		p_c_b = p['color']['b']
		p_del_tail = p['del_tail']
		point_color = Color(p_c_r, p_c_g, p_c_b)
		point_position = Position(p_x, p_y)
		point = Point(
			color=point_color,
			position=point_position,
		)
		github_link = config['github_link']
		tick = config['tick']
		bgc_r = config['background_color']['r']
		bgc_g = config['background_color']['g']
		bgc_b = config['background_color']['b']
		background_color = Color(bgc_r, bgc_g, bgc_b)
		config_obj = Config(checkpoint, point, background_color, github_link, tick, p_del_tail, cp_del_last)
		return config_obj
	