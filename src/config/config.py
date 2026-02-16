from dataclasses import dataclass

from src.config.point import Point, Color


@dataclass
class Config:
	checkpoint: Point
	point: Point
	background_color: Color
	github_link: str
	tick: int
	del_tail: bool
	del_last_checkpoints: bool
	