from wx import App
from ui.main_frame import MainFrame


app = App()
frame = MainFrame()
frame.Show()
app.MainLoop()
