import curses

from pathlib import Path

from src.app import App


CONFIG_PATH = Path(__file__).parent.parent / 'config' / 'config.json'
CONFIG_ENCODING = 'UTF-8'


def main(screen: curses.window) -> None:
	curses.curs_set(0)
	curses.raw()
	app = App(CONFIG_PATH, CONFIG_ENCODING)
	app.main(screen)

if __name__ == '__main__':
	curses.wrapper(main)
