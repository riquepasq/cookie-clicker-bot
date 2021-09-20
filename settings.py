"""
    Configuration file for easier execution
"""
BROWSER_WIDTH = 1920
BROWSER_HEIGHT = 1060

# A headless browser is a web browser without a graphical user interface
HEADLESS_BROWSER = False

# How many threads will be used to click the big cookie
NUMBER_OF_COOKIE_THREADS = 4

# Time between save export (in seconds)
SAVE_INTERVAL = 30

# Save file
SAVE_FILE = 'save.txt'

GAME_OPTIONS = {
    'Volume percentage': 0,
    'Fancy graphics': False,
    'CSS filters': False,
    'Particles': False,
    'Numbers': True,
    'Milk': False,
    'Cursors': False,
    'Wobbly cookie': False,
    'Alt cookie sound': False,
    'Icon crates': False,
    'Alt font': False,
    'Short numbers': False,  # must be 'False' to make the cookie count work
    'Fast notes': True,
    'Closing warning': False,
    'Defocus': True,
    'Extra buttons': False,
    'Lump confirmation': False,
    'Custom grandmas': False,
    'Sleep mode timeout': True
}
