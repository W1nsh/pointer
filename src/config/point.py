from dataclasses import dataclass

from src.config.position import Position
from src.config.color import Color


@dataclass
class Point:
	color: Color
	position: Position | None = None
	indent: Position | None = None
	border: Position | None = None
