import wx


if wx.Platform == '__WXMSW__':
    MAIN_FRAME_SIZE = (1000, 750)
    OPTION_DLG_SIZE = (700, 625)
    FACES = {
        'times': 'Cambria',
        'mono': 'Consolas',
        'helv': 'Calibri',
        'other': 'Segoe UI',
        'size': 11,
        'size2': 9,
    }
elif wx.Platform == '__WXMAC__':
    MAIN_FRAME_SIZE = (1000, 750)
    OPTION_DLG_SIZE = (700, 625)
    FACES = {
        'times': 'Times New Roman',
        'mono': 'Monaco',
        'helv': 'Arial',
        'other': 'Comic Sans MS',
        'size': 12,
        'size2': 10,
    }
else:   # Unix/Linux
    MAIN_FRAME_SIZE = (1100, 850)
    OPTION_DLG_SIZE = (800, 725)
    FACES = {
        'times': 'Times',
        'mono': 'Courier',
        'helv': 'Helvetica',
        'other': 'new century schoolbook',
        'size': 12,
        'size2': 10,
    }
