import wx

from generators.code_generators import CodeGenerators
from ui.platform import OPTION_DLG_SIZE
from ui.forms import OptionDialogBase
from ui.common_option_page import CommonOptionPage
from ui.java_option_page import JavaOptionPage
from ui.csharp_option_page import CSharpOptionPage
from ui.cpp_option_page import CppOptionPage
from ui.ts_option_page import TypeScriptOptionPage
from ui.sql_option_page import SqlOptionPage


class OptionDialog(OptionDialogBase):

    def __init__(self, parent, options):
        super().__init__(parent)
        self.options = options

        self.SetSize(OPTION_DLG_SIZE)

        self.txtRootPackage.SetValue(options['package'])
        self.chkGenerateDefaultCtor.SetValue(options['generate']['default_ctor'])
        self.chkGenerateFullArgCtor.SetValue(options['generate']['full_arg_ctor'])
        self.chkGenerateEqHc.SetValue(options['generate']['equal_hashcode'])
        self.chkGenerateToString.SetValue(options['generate']['to_string'])
        self.chkEncapsulateAllProps.SetValue(options['encapsulate_all_props'])

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
            'language_specific': language_specific,
        }

    def dialogButtonSizerOnCancelButtonClick(self, event):
        self.EndModal(wx.ID_CANCEL)

    def dialogButtonSizerOnOKButtonClick(self, event):
        self.dialogButtonSizerOnApplyButtonClick(event)
        self.EndModal(wx.ID_OK)
