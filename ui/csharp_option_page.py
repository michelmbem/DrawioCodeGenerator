from ui.forms import CSharpOptionPageBase
from ui.option_page_with_import import OptionPageWithImports


class CSharpOptionPage(CSharpOptionPageBase, OptionPageWithImports):

    def __init__(self, parent, options):
        CSharpOptionPageBase.__init__(self, parent)
        OptionPageWithImports.__init__(self, "cs", options)

        self.chkAddEFCoreAttrib.SetValue(options['add_efcore'])

    @property
    def options(self):
        return {
            'add_efcore': self.chkAddEFCoreAttrib.IsChecked(),
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
