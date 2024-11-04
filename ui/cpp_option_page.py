from ui.forms import CppOptionPageBase
from ui.option_page_with_import import OptionPageWithImports


class CppOptionPage(CppOptionPageBase, OptionPageWithImports):

    NAMING_CONVENTIONS = ["pascal", "camel", "snake"]

    def __init__(self, parent, options):
        CppOptionPageBase.__init__(self, parent)
        OptionPageWithImports.__init__(self, "cpp", options)

        self.chkUseBoost.SetValue(options['use_boost'])
        self.chcNamingConvention.SetSelection(self.NAMING_CONVENTIONS.index(options['naming']))
        self.chkLBraceOnSameLine.SetValue(options['lbrace_same_line'])

    @property
    def options(self):
        return {
            'use_boost': self.chkUseBoost.IsChecked(),
            'naming': self.NAMING_CONVENTIONS[self.chcNamingConvention.GetSelection()],
            'lbrace_same_line': self.chkLBraceOnSameLine.IsChecked(),
            **super().options
        }

    def asset_path(self, bitmap_path):
        return OptionPageWithImports.asset_path(self, bitmap_path)

    def lscImportOnListItemSelected(self, event):
        OptionPageWithImports.lscImportOnListItemSelected(self, event)

    def btnAddImportOnButtonClick(self, event):
        OptionPageWithImports.btnAddImportOnButtonClick(self, event)

    def btnUpdateImportOnButtonClick( self, event ):
        OptionPageWithImports.btnUpdateImportOnButtonClick(self, event)

    def btnRemoveImportOnButtonClick(self, event):
        OptionPageWithImports.btnRemoveImportOnButtonClick(self, event)
