import sys
import wx

from os import path, startfile
from io import StringIO
from decode.convert_to_readable import DecodeAndDecompress
from parsers.style_parser import StyleParser
from parsers.syntax_parser import SyntaxParser
from generators.code_generators import CodeGenerators
from ui.forms import MainFrameBase
from ui.xml_styled_text_ctrl import XMLStyledTextCtrl
from ui.symbol_tree_ctrl import SymbolTreeCtrl
from ui.options_dialog import OptionDialog
from bs4 import BeautifulSoup as bs


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

        self.tlcStyle = SymbolTreeCtrl(self.nbTrees)
        self.nbTrees.AddPage(self.tlcStyle, "Style tree")

        self.tlcSyntax = SymbolTreeCtrl(self.nbTrees)
        self.nbTrees.AddPage(self.tlcSyntax, "Syntax tree")

        self.options = self._default_options()

        self._original_stdout = sys.stdout
        sys.stdout = self._captured_output = StringIO()

    def __del__(self):
        MainFrameBase.__del__(self)
        sys.stdout = self._original_stdout

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

    def btnLangOptionsOnButtonClick(self, event):
        option_dialog = OptionDialog(self, self.options)
        if option_dialog.ShowModal() == wx.ID_OK:
            self.options = option_dialog.options

    def btnGenerateOnButtonClick(self, event):
        message = None

        try:
            decoded_xml = DecodeAndDecompress.convert(self.txtDiagramPath.GetValue())
            if not decoded_xml:
                message = "Failed to decode diagram XML"
                return

            self.stcDecodedXml.SetReadOnly(False)
            self.stcDecodedXml.SetValue(bs(decoded_xml, "lxml").prettify())
            self.stcDecodedXml.SetReadOnly(True)

            style_parser = StyleParser(decoded_xml)
            style_tree = style_parser.convert_to_style_tree()
            self.tlcStyle.load_dict(style_tree)

            syntax_parser = SyntaxParser(style_tree)
            syntax_tree = syntax_parser.convert_to_syntax_tree()
            self.tlcSyntax.load_dict(syntax_tree)

            language_selected = False

            for item in self.chkLangTS.GetContainingSizer().GetChildren():
                checkbox = item.GetWindow()
                if checkbox.IsChecked():
                    language = checkbox.GetLabel()
                    output_dir = path.join(self.txtOutputPath.GetValue(), language)
                    code_gen = CodeGenerators.get(language, syntax_tree, output_dir, self.options)
                    code_gen.generate_code()
                    language_selected = True

            if language_selected:
                startfile(path.abspath(self.txtOutputPath.GetValue()))
            else:
                message = "No language was selected!"
        except Exception as e:
            message = f"Something went wrong: {e}"
        finally:
            self.rtcStdout.SetValue(self._captured_output.getvalue())
            self.rtcStdout.ShowPosition(self.rtcStdout.GetLastPosition())

            if message:
                wx.MessageBox(message, "Code generation")

    def btnExitOnButtonClick(self, event):
        self.Close()
        self.Destroy()

    def asset_path(self, bitmap_path):
        return path.join(path.dirname(__file__), bitmap_path)

    @staticmethod
    def _default_options():
        return {
            'package': "com.example",
            'generate': {
                'default_ctor': False,
                'full_arg_ctor': False,
                'equal_hashcode': False,
                'to_string': False
            },
            'encapsulate_all_props': False,
            'language_specific': {
                'java': {
                    'imports': {
                        'java.math': ["BigInteger", "BigDecimal"],
                        'java.time': ["LocalDate", "LocalTime", "LocalDateTime"],
                        'java.util': ["Objects"],
                    }
                },
                'cs': {
                    'imports': {
                        'System': None,
                        'System.Numerics': None,
                    }
                },
                'cpp': {
                    'imports': {
                        '<ctime>': None,
                        '<string>': None,
                    }
                },
                'python': {},
                'ts': {},
                'php': {},
                'sql': {},
            },
        }
