import wx


class OptionPage:

    def __init__(self):
        if wx.SystemSettings.GetAppearance().IsUsingDarkBackground():
            self.line_colors = (wx.Colour(0x334433), wx.Colour(0x222222))
        else:
            self.line_colors = (wx.Colour(0xDDEEDD), wx.Colour(0xFFFFFF))

    @property
    def language(self):
        return None

    @property
    def options(self):
        return {}
