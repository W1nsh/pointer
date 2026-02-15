import curses

from src.app import App


CONFIG_PATH = 'src\\config\\config.json' # Write your full path to config.json
CONFIG_ENCODING = 'UTF-8'


def main(screen: curses.window) -> None:
	curses.curs_set(0)
	curses.raw()
	app = App(CONFIG_PATH, CONFIG_ENCODING)
	app.main(screen)

if __name__ == '__main__':
	curses.wrapper(main)
