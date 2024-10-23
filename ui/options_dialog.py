import wx

from ui.forms import OptionDialogBase
from ui.lang_option_page import LanguageOptionPage


class OptionDialog(OptionDialogBase):

    def __init__(self, parent, options):
        OptionDialogBase.__init__(self, parent)
        self._options = options

        self.txtRootPackage.SetValue(options['package'])
        self.chkGenerateDefaultCtor.SetValue(options['generate']['default_ctor'])
        self.chkGenerateFullArgCtor.SetValue(options['generate']['full_arg_ctor'])
        self.chkGenerateEqHc.SetValue(options['generate']['equal_hashcode'])
        self.chkGenerateToString.SetValue(options['generate']['to_string'])
        self.chkEncapsulateAllProps.SetValue(options['encapsulate_all_props'])

        language_specific = options['language_specific']
        languages = ["Java", "C#", "C++", "Python", "TypeScript", "PHP", "SQL"]

        for language in languages:
            language_options = language_specific.get(language, {})
            option_page = LanguageOptionPage(self.nbLanguageOptions, language, language_options)
            self.nbLanguageOptions.AddPage(option_page, language)

        # self.DoLayoutAdaptation()

    @property
    def options(self):
        return self._options

    def dialogButtonSizerOnApplyButtonClick(self, event):
        language_options = {}

        for i in range(self.nbLanguageOptions.PageCount):
            option_page = self.nbLanguageOptions.GetPage(i)
            language_options[option_page.language] = option_page.options

        self._options = {
            'package': self.txtRootPackage.GetValue(),
            'generate': {
                'default_ctor': self.chkGenerateDefaultCtor.IsChecked(),
                'full_arg_ctor': self.chkGenerateFullArgCtor.IsChecked(),
                'equal_hashcode': self.chkGenerateEqHc.IsChecked(),
                'to_string': self.chkGenerateToString.IsChecked(),
            },
            'encapsulate_all_props': self.chkEncapsulateAllProps.IsChecked(),
            'language_specific': language_options,
        }

    def dialogButtonSizerOnCancelButtonClick(self, event):
        self.EndModal(wx.ID_CANCEL)

    def dialogButtonSizerOnOKButtonClick(self, event):
        self.dialogButtonSizerOnApplyButtonClick(event)
        self.EndModal(wx.ID_OK)
