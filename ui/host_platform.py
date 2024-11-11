# Importing the standard 'platform' module, not this module!
import platform
import wx


match platform.system():
    case "Windows":
        SIZE_DELTA = (0, 0)
        FACES = {
            'serif': 'Cambria',
            'sans-serif': 'Calibri',
            'mono': 'Consolas',
            'other': 'Comic Sans MS',
            'medium': 11,
        }
    case "Darwin":
        SIZE_DELTA = (0, 0)
        FACES = {
            'serif': 'Times New Roman',
            'sans-serif': 'Arial',
            'mono': 'Monaco',
            'other': 'Comic Sans MS',
            'medium': 12,
        }
    case _:   # Unix/Linux
        SIZE_DELTA = (100, 100)
        FACES = {
            'serif': 'Times',
            'sans-serif': 'Helvetica',
            'mono': 'Courier',
            'other': 'new century schoolbook',
            'medium': 12,
        }

        os_release = platform.freedesktop_os_release()
        if os_release['NAME'] == "Ubuntu":
            FACES['mono'] = 'Ubuntu Mono'


FACES['sanserif'] = FACES['sans-serif']

FACES['large'] = FACES['medium'] + 2
FACES['larger'] = FACES['large'] + 2
FACES['largest'] = FACES['larger'] + 2

FACES['small'] = FACES['medium'] - 2
FACES['smaller'] = FACES['small'] - 2
FACES['smallest'] = FACES['smaller'] - 2


def adjust_window_to_display(window):
    x, y = window.GetPosition()
    width, height = window.GetSize()
    screen_width, screen_height = wx.DisplaySize()

    width += SIZE_DELTA[0]
    if width > screen_width:
        x, width = 0, screen_width

    height += SIZE_DELTA[1]
    if height > screen_height:
        y, height = 0, screen_height

    window.SetPosition((x, y))
    window.SetSize(width, height)
