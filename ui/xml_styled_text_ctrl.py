import wx
import wx.stc as stc

from bs4 import BeautifulSoup as bs
from ui.host_platform import FACES


class XMLStyledTextCtrl(stc.StyledTextCtrl):

    def __init__(self, parent):
        super().__init__(parent)

        if wx.SystemSettings.GetAppearance().IsUsingDarkBackground():
            colors = {'fg':  '#EEEEEE', 'bg': '#222222', 'tag': '#5599FF', 'att': '#FF5555', 'str': '#55FF99', 'fold': '#C3C3C3'}
        else:
            colors = {'fg':  'black', 'bg': 'white', 'tag': '#0000CC', 'att': '#990000', 'str': '#009900', 'fold': '#808080'}

        # Set the lexer to XML
        self.SetLexer(stc.STC_LEX_XML)

        # Global default styles for all languages
        self.StyleResetDefault()
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT, "fore:{fg},back:{bg},face:{mono},size:{medium}".format(**FACES, **colors))
        self.StyleClearAll()

        # Set styles for XML elements
        self.StyleSetSpec(stc.STC_H_TAG, "fore:%(tag)s,bold" % colors)
        self.StyleSetSpec(stc.STC_H_ATTRIBUTE, "fore:%(att)s" % colors)
        self.StyleSetSpec(stc.STC_H_DOUBLESTRING, "fore:%(str)s" % colors)

        # Enable folding
        self.SetProperty("fold", "1")
        self.SetProperty("fold.html", "1")
        self.SetMarginType(2, stc.STC_MARGIN_SYMBOL)
        self.SetMarginMask(2, stc.STC_MASK_FOLDERS)
        self.SetMarginSensitive(2, True)
        self.SetMarginWidth(2, 12)

        # Define markers for folding
        self.MarkerDefine(stc.STC_MARKNUM_FOLDER, stc.STC_MARK_BOXPLUS, colors['bg'], colors['fold'])
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN, stc.STC_MARK_BOXMINUS, colors['bg'], colors['fold'])
        self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB, stc.STC_MARK_VLINE, colors['bg'], colors['fold'])
        self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL, stc.STC_MARK_LCORNER, colors['bg'], colors['fold'])
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND, stc.STC_MARK_BOXPLUSCONNECTED, colors['bg'], colors['fold'])
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_BOXMINUSCONNECTED, colors['bg'], colors['fold'])
        self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNER, colors['bg'], colors['fold'])

        # Listen for clics on margins
        self.Bind(stc.EVT_STC_MARGINCLICK, self.onMarginClick)

    @property
    def xml_content(self):
        return self.GetValue()

    @xml_content.setter
    def xml_content(self, content):
        read_only = self.GetReadOnly()
        self.SetReadOnly(False)

        if content:
            self.SetValue(bs(content, "lxml").prettify())
        else:
            self.ClearAll()

        self.SetReadOnly(read_only)

    def onMarginClick(self, event):
        # Fold or unfold the corresponding line
        self.ToggleFold(self.LineFromPosition(event.GetPosition()))
