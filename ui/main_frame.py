import sys
import wx
import wx.adv as adv

from os import path
from io import StringIO
from startfile import startfile
from decode.convert_to_readable import DecodeAndDecompress
from parsers.style_parser import StyleParser
from parsers.syntax_parser import SyntaxParser
from generators.code_generators import CodeGenerators
from ui.host_platform import FACES, adjust_window_to_display
from ui.persistent_window import PersistentWindow
from ui.forms import MainFrameBase
from ui.xml_styled_text_ctrl import XMLStyledTextCtrl
from ui.symbol_tree_ctrl import SymbolTreeCtrl
from ui.options_dialog import OptionDialog


class MainFrame (MainFrameBase, PersistentWindow):

    def __init__(self):
        MainFrameBase.__init__(self, None)
        PersistentWindow.__init__(self, "main_frame.json")
        self.syntax_tree = None
        self.options = self.default_options()
        self.original_stdout = sys.stdout
        self.captured_output = sys.stdout = StringIO()

        self.SetIcon(wx.Icon(self.asset_path(u"assets/icons/app-icon.png"), wx.BITMAP_TYPE_PNG))
        adjust_window_to_display(self)
        self.load_settings()

        image_list = wx.ImageList(16, 16)
        image_list.Add(wx.Bitmap(self.asset_path(u"assets/icons/page_white_code.png"), wx.BITMAP_TYPE_PNG))
        image_list.Add(wx.Bitmap(self.asset_path(u"assets/icons/node-tree.png"), wx.BITMAP_TYPE_PNG))
        self.nbTrees.AssignImageList(image_list)

        self.stcDecodedXml = XMLStyledTextCtrl(self.nbTrees)
        self.nbTrees.AddPage(self.stcDecodedXml, "Decoded XML", True, 0)

        self.tlcStyle = SymbolTreeCtrl(self.nbTrees)
        self.nbTrees.AddPage(self.tlcStyle, "Style tree", imageId=1)

        self.tlcSyntax = SymbolTreeCtrl(self.nbTrees)
        self.nbTrees.AddPage(self.tlcSyntax, "Syntax tree", imageId=1)

        self.rtcStdout.SetFont(wx.Font(wx.FontInfo(FACES['medium']).FaceName(FACES['mono'])))

        self.fpcDiagramPath.SetPath("examples/simple_class_diagram.drawio")
        self.fpcDiagramPathOnFileChanged(None)

    def __del__(self):
        super().__del__()
        sys.stdout = self.original_stdout

    @staticmethod
    def default_options():
        return {
            'package': "com.example",
            'generate': {
                'default_ctor': False,
                'full_arg_ctor': False,
                'equal_hashcode': False,
                'to_string': False
            },
            'encapsulate_all_props': False,
            'infer_keys': False,
            'pk_pattern': "^(@class)?_?(id|pk|key)$",
            'language_specific': {
                'java': {
                    'use_lombok': False,
                    'add_builder': False,
                    'add_jpa': False,
                    'use_jakarta': False,
                    'temporal_types': "java8_local",
                    'imports': {
                        'java.math': ["BigInteger", "BigDecimal"],
                        'java.util': ["Objects", "Set", "HashSet", "UUID"],
                    }
                },
                'cs': {
                    'add_efcore': False,
                    'imports': {
                        'System': None,
                        'System.Collections.Generic': None,
                        'System.Numerics': None,
                    }
                },
                'cpp': {
                    'use_boost': False,
                    'naming': "pascal",
                    'lbrace_same_line': False,
                    'imports': {
                        '<ctime>': None,
                        '<string>': ["std::string", "std::wstring"],
                        '<array>': ["std::array"],
                        '<vector>': ["std::vector"],
                    },
                },
                'python': {
                    'imports': {},
                },
                'ts': {
                    'optional_props': True,
                    'imports': {},
                },
                'php': {
                    'imports': {},
                },
                'sql': {
                    'dialect': "ansi",
                    'single_script': True,
                    'filename': "database",
                },
            },
        }


    def update_log(self):
        self.rtcStdout.SetValue(self.captured_output.getvalue())
        self.rtcStdout.ShowPosition(self.rtcStdout.GetLastPosition())

    def asset_path(self, bitmap_path):
        return path.join(path.dirname(__file__), bitmap_path)

    def MainFrameBaseOnClose(self, event):
        self.save_settings()
        event.Skip()

    def fpcDiagramPathOnFileChanged(self, event):
        self.dpcOutputDir.SetPath(path.join(path.dirname(self.fpcDiagramPath.GetPath()), "src"))
        self.syntax_tree = None
        self.stcDecodedXml.xml_content = None
        self.tlcStyle.load_dict(None)
        self.tlcSyntax.load_dict(None)

    def btnLangOptionsOnButtonClick(self, event):
        option_dialog = OptionDialog(self, self.options)
        if option_dialog.ShowModal() == wx.ID_OK:
            self.options = option_dialog.options


    def btnAboutOnButtonClick(self, event):
        info = adv.AboutDialogInfo()

        info.SetIcon(wx.Icon(self.asset_path(u"assets/icons/app-icon-small.png"), wx.BITMAP_TYPE_PNG))
        info.SetName("Drawio Code Generator")
        info.SetVersion("1.0.1")
        info.SetDescription("Generate source code in different programming\nlanguages from a draw.io UML class diagram")
        info.SetCopyright("(c) 2024 Michel Mbem")
        info.SetWebSite("https://github.com/michelmbem/DrawioCodeGenerator")
        info.AddDeveloper("Michel Mbem<michel.mbem@gmail.com>")

        adv.AboutBox(info)

    def btnParseOnButtonClick(self, event):
        message = None

        try:
            decoded_xml = DecodeAndDecompress.convert(self.fpcDiagramPath.GetPath())

            if decoded_xml:
                self.stcDecodedXml.xml_content = decoded_xml

                style_parser = StyleParser(decoded_xml)
                style_tree = style_parser.convert_to_style_tree()
                self.tlcStyle.load_dict(style_tree)

                syntax_parser = SyntaxParser(style_tree)
                self.syntax_tree = syntax_parser.convert_to_syntax_tree()
                self.tlcSyntax.load_dict(self.syntax_tree)
            else:
                message = "Failed to decode diagram's XML"
        except Exception as e:
            message = f"Something went wrong: {e}"
        finally:
            self.update_log()

            if message:
                wx.MessageBox(message, "Diagram parsing error", wx.OK | wx.ICON_ERROR)

    def btnGenerateOnButtonClick(self, event):
        if not self.syntax_tree:
            self.btnParseOnButtonClick(None)
            if not self.syntax_tree:
                return

        selected_languages = set()
        for item in self.chkLangTS.GetContainingSizer().GetChildren():
            checkbox = item.GetWindow()
            if isinstance(checkbox, wx.CheckBox) and checkbox.IsChecked():
                selected_languages.add(checkbox.GetLabel())

        selected_language_count = len(selected_languages)
        if selected_language_count <= 0:
            wx.MessageBox("No language was selected for code generation!",
                          "Code generation aborted",
                          wx.OK | wx.ICON_WARNING)
            return

        try:
            for language in selected_languages:
                out_dir = self.dpcOutputDir.GetPath()
                if selected_language_count > 1:
                    out_dir = path.join(out_dir, language)
                code_gen = CodeGenerators.get(language, self.syntax_tree, out_dir, self.options)
                code_gen.generate_code()

            startfile(path.abspath(self.dpcOutputDir.GetPath()))
        except Exception as e:
            wx.MessageBox(f"Something went wrong: {e}",
                          "Code generation error",
                          wx.OK | wx.ICON_ERROR)
        finally:
            self.update_log()

    def btnExitOnButtonClick(self, event):
        self.Close()
        self.Destroy()
