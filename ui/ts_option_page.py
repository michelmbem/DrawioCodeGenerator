from ui.forms import TypeScriptOptionPageBase
from ui.option_page_with_import import OptionPageWithImports


class TypeScriptOptionPage(TypeScriptOptionPageBase, OptionPageWithImports):

    def __init__(self, parent, options):
        TypeScriptOptionPageBase.__init__(self, parent)
        OptionPageWithImports.__init__(self, "ts", options)

        self.chkOptionalProps.SetValue(options['optional_props'])

    @property
    def options(self):
        return {
            'optional_props': self.chkOptionalProps.IsChecked(),
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
