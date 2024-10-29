from ui.forms import CommonOptionPageBase
from ui.option_page_with_import import OptionPageWithImports


class CommonOptionPage(CommonOptionPageBase, OptionPageWithImports):

    def __init__(self, parent, language, options):
        CommonOptionPageBase.__init__(self, parent)
        OptionPageWithImports.__init__(self, language, options)

    def btnAddModuleOnButtonClick(self, event):
        OptionPageWithImports.btnAddModuleOnButtonClick(self, event)

    def btnRemoveModuleOnButtonClick(self, event):
        OptionPageWithImports.btnRemoveModuleOnButtonClick(self, event)
