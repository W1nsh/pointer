from dataclasses import dataclass

from src.config.point import Point


@dataclass
class Config:
	checkpoint: Point
	point: Point
	github_link: str
	tick: int
	del_tail: bool
	del_last_checkpoints: bool
