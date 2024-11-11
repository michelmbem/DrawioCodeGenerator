# Importing the standard 'platform' module, not this module!
import platform
import wx


def fit_size(size):
    width, height = size
    screen_width, screen_height = wx.DisplaySize()
    if width > screen_width: width = screen_width
    if height > screen_height: height = screen_height
    return width, height


OS_NAME = platform.system()

if OS_NAME == "Windows":
    MAIN_FRAME_SIZE = (1000, 750)
    OPTION_DLG_SIZE = (700, 700)
    FACES = {
        'serif': 'Cambria',
        'sans-serif': 'Calibri',
        'mono': 'Consolas',
        'other': 'Comic Sans MS',
        'medium': 11,
    }
elif OS_NAME == "Darwin":
    MAIN_FRAME_SIZE = (1000, 750)   # Check on a Mac
    OPTION_DLG_SIZE = (700, 700)    # Check on a Mac
    FACES = {
        'serif': 'Times New Roman',
        'sans-serif': 'Arial',
        'mono': 'Monaco',
        'other': 'Comic Sans MS',
        'medium': 12,
    }
else:   # Unix/Linux
    OS_RELEASE = platform.freedesktop_os_release()
    MAIN_FRAME_SIZE = (1100, 850)
    OPTION_DLG_SIZE = (800, 800)
    FACES = {
        'serif': 'Times',
        'sans-serif': 'Helvetica',
        'mono': 'Courier',
        'other': 'new century schoolbook',
        'medium': 12,
    }

    if OS_RELEASE['NAME'] == "Ubuntu":
        FACES['mono'] = 'Ubuntu Mono'


FACES['sanserif'] = FACES['sans-serif']

FACES['large'] = FACES['medium'] + 2
FACES['larger'] = FACES['large'] + 2
FACES['largest'] = FACES['larger'] + 2

FACES['small'] = FACES['medium'] - 2
FACES['smaller'] = FACES['small'] - 2
FACES['smallest'] = FACES['smaller'] - 2
