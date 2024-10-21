from wx import App
from ui.mainframe import MainFrame


app = App()
frame = MainFrame()
frame.Show()
app.MainLoop()
