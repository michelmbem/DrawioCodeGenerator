from ui.forms import CSharpOptionPageBase
from ui.option_page_with_import import OptionPageWithImports


class CSharpOptionPage(CSharpOptionPageBase, OptionPageWithImports):

    def __init__(self, parent, options):
        CSharpOptionPageBase.__init__(self, parent)
        OptionPageWithImports.__init__(self, "cs", options)

        self.chkAddEFCoreAttrib.SetValue(options.get('add_jpa', False))

    @property
    def options(self):
        return {
            'add_efcore': self.chkAddEFCoreAttrib.IsChecked(),
            **super().options
        }

    def btnAddModuleOnButtonClick(self, event):
        OptionPageWithImports.btnAddModuleOnButtonClick(self, event)

    def btnRemoveModuleOnButtonClick(self, event):
        OptionPageWithImports.btnRemoveModuleOnButtonClick(self, event)
