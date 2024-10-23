import wx
import wx.stc as stc


class XMLStyledTextCtrl(stc.StyledTextCtrl):
    def __init__(self, parent):
        super().__init__(parent)

        # Set the lexer to XML
        self.SetLexer(stc.STC_LEX_XML)

        # Global default styles for all languages
        self.StyleResetDefault()
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT, "face:%(mono)s,size:%(size)d" % faces)
        self.StyleClearAll()

        # Set styles for XML elements
        self.StyleSetSpec(stc.STC_H_TAG, "fore:#0000CC,bold")
        self.StyleSetSpec(stc.STC_H_ATTRIBUTE, "fore:#990000")
        self.StyleSetSpec(stc.STC_H_DOUBLESTRING, "fore:#009900")

        # Enable folding
        self.SetProperty("fold", "1")
        self.SetProperty("fold.html", "1")
        self.SetMarginType(2, stc.STC_MARGIN_SYMBOL)
        self.SetMarginMask(2, stc.STC_MASK_FOLDERS)
        self.SetMarginSensitive(2, True)
        self.SetMarginWidth(2, 12)

        # Define markers for folding
        self.MarkerDefine(stc.STC_MARKNUM_FOLDER, stc.STC_MARK_BOXPLUS, "white", "#808080")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN, stc.STC_MARK_BOXMINUS, "white", "#808080")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB, stc.STC_MARK_VLINE, "white", "#808080")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL, stc.STC_MARK_LCORNER, "white", "#808080")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND, stc.STC_MARK_BOXPLUSCONNECTED, "white", "#808080")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_BOXMINUSCONNECTED, "white", "#808080")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNER, "white", "#808080")


# ========================= Initialization ========================


if wx.Platform == '__WXMSW__':
    faces = {
        'times': 'Cambria',
        'mono': 'Consolas',
        'helv': 'Calibri',
        'other': 'Segoe UI',
        'size': 11,
        'size2': 9,
    }
elif wx.Platform == '__WXMAC__':
    faces = {
        'times': 'Times New Roman',
        'mono': 'Monaco',
        'helv': 'Arial',
        'other': 'Comic Sans MS',
        'size': 12,
        'size2': 10,
    }
else:   # Unix/Linux
    faces = {
        'times': 'Times',
        'mono': 'Courier',
        'helv': 'Helvetica',
        'other': 'new century schoolbook',
        'size': 12,
        'size2': 10,
    }
