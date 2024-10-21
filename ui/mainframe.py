import wx
from os import path, startfile
from bs4 import BeautifulSoup
from decode.convert_to_readable import DecodeAndDecompress
from parsers.style_parser import StyleParser
from parsers.syntax_parser import SyntaxParser
from generators.code_generators import CodeGenerators
from ui.forms import MainFrameBase
from ui.xmlstyledtextctrl import XMLStyledTextCtrl
from ui.symboltreectrl import SymbolTreeCtrl


class MainFrame (MainFrameBase):

    def __init__(self):
        MainFrameBase.__init__(self, None)

        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap(self.asset_path(u"assets/icons/drawio-icon.png"), wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)

        self.txtDiagramPath.SetValue("examples/simple_class_diagram.drawio")
        self.txtOutputPath.SetValue("examples/sources")

        self.stcDecodedXml = XMLStyledTextCtrl(self.nbTrees)
        self.nbTrees.AddPage(self.stcDecodedXml, "Decoded XML", True)

        self.trcStyle = SymbolTreeCtrl(self.nbTrees)
        self.nbTrees.AddPage(self.trcStyle, "Style tree")

        self.trcSyntax = SymbolTreeCtrl(self.nbTrees)
        self.nbTrees.AddPage(self.trcSyntax, "Syntax tree")

    def btnChooseDiagramPathOnButtonClick(self, event):
        open_file_dialog = wx.FileDialog(self, message="Open a diagram",
                                         wildcard="Draw.io diagram files (*.drawio)|*.drawio",
                                         style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if open_file_dialog.ShowModal() == wx.ID_OK:
            self.txtDiagramPath.SetValue(open_file_dialog.GetPath())
            self.txtOutputPath.SetValue(path.dirname(open_file_dialog.GetPath()))

        open_file_dialog.Destroy()

    def btnChooseOutputPathOnButtonClick(self, event):

        dir_dialog = wx.DirDialog(self, message="Select output directory",
                                  defaultPath=self.txtOutputPath.GetValue(),
                                  style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)

        if dir_dialog.ShowModal() == wx.ID_OK:
            self.txtOutputPath.SetValue(dir_dialog.GetPath())

        dir_dialog.Destroy()

    def btnGenerateOnButtonClick(self, event):
        decoded_xml = DecodeAndDecompress.convert(self.txtDiagramPath.GetValue())
        if not decoded_xml:
            wx.MessageBox("Failed to decode diagram XML", "Code generation")
            return

        pretty_xml = BeautifulSoup(decoded_xml, "lxml").prettify()
        self.stcDecodedXml.SetReadOnly(False)
        self.stcDecodedXml.SetValue(pretty_xml)
        self.stcDecodedXml.SetReadOnly(True)

        style_parser = StyleParser(decoded_xml)
        style_tree = style_parser.convert_to_style_tree()
        self.trcStyle.load_dict(style_tree)

        syntax_parser = SyntaxParser(style_tree)
        syntax_tree = syntax_parser.convert_to_syntax_tree()
        self.trcSyntax.load_dict(syntax_tree)

        language_selected = False

        for item in self.chkLangTS.GetContainingSizer().GetChildren():
            checkbox = item.GetWindow()
            if checkbox.IsChecked():
                language = checkbox.GetLabel()
                output_dir = path.join(self.txtOutputPath.GetValue(), language)
                code_gen = CodeGenerators.create(language, syntax_tree, output_dir)
                code_gen.generate_code()
                language_selected = True

        if language_selected:
            startfile(path.abspath(self.txtOutputPath.GetValue()))
        else:
            wx.MessageBox("No language was selected!", "Code generation")

    def btnExitOnButtonClick(self, event):
        self.Close()
        self.Destroy()

    def asset_path(self, bitmap_path):
        return path.join(path.dirname(__file__), bitmap_path)
