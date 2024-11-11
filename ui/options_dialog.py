import wx

from generators.code_generators import CodeGenerators
from ui.platform import OPTION_DLG_SIZE, fit_size
from ui.persistent_window import PersistentWindow
from ui.forms import OptionDialogBase
from ui.common_option_page import CommonOptionPage
from ui.java_option_page import JavaOptionPage
from ui.csharp_option_page import CSharpOptionPage
from ui.cpp_option_page import CppOptionPage
from ui.ts_option_page import TypeScriptOptionPage
from ui.sql_option_page import SqlOptionPage


class OptionDialog(OptionDialogBase, PersistentWindow):

    def __init__(self, parent, options):
        OptionDialogBase.__init__(self, parent)
        PersistentWindow.__init__(self, "option_dialog.json")
        self.options = options

        self.SetSize(fit_size(OPTION_DLG_SIZE))
        self.load_settings()

        self.txtRootPackage.SetValue(options['package'])
        self.chkGenerateDefaultCtor.SetValue(options['generate']['default_ctor'])
        self.chkGenerateFullArgCtor.SetValue(options['generate']['full_arg_ctor'])
        self.chkGenerateEqHc.SetValue(options['generate']['equal_hashcode'])
        self.chkGenerateToString.SetValue(options['generate']['to_string'])
        self.chkEncapsulateAllProps.SetValue(options['encapsulate_all_props'])
        self.chkEncapsulateAllProps.SetValue(options['encapsulate_all_props'])
        self.chkInferKeys.SetValue(options['infer_keys'])
        self.txtPKPattern.SetValue(options['pk_pattern'])
        self.chkInferKeysOnCheckBox(None)

        language_specific = options['language_specific']
        languages = ["java", "cs", "cpp", "python", "ts", "php", "sql"]

        for language in languages:
            language_options = language_specific.get(language, {})

            match language:
                case 'java':
                    option_page = JavaOptionPage(self.nbLanguageOptions, language_options)
                case 'cs':
                    option_page = CSharpOptionPage(self.nbLanguageOptions, language_options)
                case 'cpp':
                    option_page = CppOptionPage(self.nbLanguageOptions, language_options)
                case 'ts':
                    option_page = TypeScriptOptionPage(self.nbLanguageOptions, language_options)
                case "sql":
                    option_page = SqlOptionPage(self.nbLanguageOptions, language_options)
                case _:
                    option_page = CommonOptionPage(self.nbLanguageOptions, language, language_options)

            self.nbLanguageOptions.AddPage(option_page, CodeGenerators.language_name(language))

    def OptionDialogBaseOnClose(self, event):
        self.save_settings()

    def chkInferKeysOnCheckBox(self, event):
        self.txtPKPattern.Enable(self.chkInferKeys.IsChecked())

    def dialogButtonSizerOnApplyButtonClick(self, event):
        language_specific = {}

        for page_index in range(self.nbLanguageOptions.PageCount):
            option_page = self.nbLanguageOptions.GetPage(page_index)
            language_specific[option_page.language] = option_page.options

        self.options = {
            'package': self.txtRootPackage.GetValue(),
            'generate': {
                'default_ctor': self.chkGenerateDefaultCtor.IsChecked(),
                'full_arg_ctor': self.chkGenerateFullArgCtor.IsChecked(),
                'equal_hashcode': self.chkGenerateEqHc.IsChecked(),
                'to_string': self.chkGenerateToString.IsChecked(),
            },
            'encapsulate_all_props': self.chkEncapsulateAllProps.IsChecked(),
            'infer_keys': self.chkInferKeys.IsChecked(),
            'pk_pattern': self.txtPKPattern.GetValue(),
            'language_specific': language_specific,
        }

    def dialogButtonSizerOnCancelButtonClick(self, event):
        self.EndModal(wx.ID_CANCEL)

    def dialogButtonSizerOnOKButtonClick(self, event):
        self.dialogButtonSizerOnApplyButtonClick(event)
        self.EndModal(wx.ID_OK)
