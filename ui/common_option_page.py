from ui.forms import CommonOptionPageBase
from ui.option_page_with_import import OptionPageWithImports


class CommonOptionPage(CommonOptionPageBase, OptionPageWithImports):

    def __init__(self, parent, language, options):
        CommonOptionPageBase.__init__(self, parent)
        OptionPageWithImports.__init__(self, language, options)

    def asset_path(self, bitmap_path):
        return OptionPageWithImports.asset_path(self, bitmap_path)

    def lscImportOnListItemSelected(self, event):
        OptionPageWithImports.lscImportOnListItemSelected(self, event)

    def btnAddModuleOnButtonClick(self, event):
        OptionPageWithImports.btnAddModuleOnButtonClick(self, event)

    def btnUpdateImportOnButtonClick( self, event ):
        OptionPageWithImports.btnUpdateImportOnButtonClick(self, event)

    def btnRemoveModuleOnButtonClick(self, event):
        OptionPageWithImports.btnRemoveModuleOnButtonClick(self, event)
