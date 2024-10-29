from ui.forms import JavaOptionPageBase
from ui.option_page_with_import import OptionPageWithImports


class JavaOptionPage(JavaOptionPageBase, OptionPageWithImports):

    def __init__(self, parent, options):
        JavaOptionPageBase.__init__(self, parent)
        OptionPageWithImports.__init__(self, "java", options)

        self.chkUseLombok.SetValue(options.get('use_lombok', False))
        self.chkUseLombokOnCheckBox(None)
        self.chkAddBuilderAnno.SetValue(options.get('add_builder', False))
        self.chkAddJpaAnno.SetValue(options.get('add_jpa', False))

    @property
    def options(self):
        return {
            'use_lombok': self.chkUseLombok.IsChecked(),
            'add_builder': self.chkAddBuilderAnno.IsChecked(),
            'add_jpa': self.chkAddJpaAnno.IsChecked(),
            **super().options
        }

    def asset_path(self, bitmap_path):
        return OptionPageWithImports.asset_path(self, bitmap_path)

    def chkUseLombokOnCheckBox(self, event):
        if self.chkUseLombok.IsChecked():
            self.chkAddBuilderAnno.Enable(True)
        else:
            self.chkAddBuilderAnno.SetValue(False)
            self.chkAddBuilderAnno.Enable(False)

    def lscImportOnListItemSelected(self, event):
        OptionPageWithImports.lscImportOnListItemSelected(self, event)

    def btnAddModuleOnButtonClick(self, event):
        OptionPageWithImports.btnAddModuleOnButtonClick(self, event)

    def btnUpdateImportOnButtonClick( self, event ):
        OptionPageWithImports.btnUpdateImportOnButtonClick(self, event)

    def btnRemoveModuleOnButtonClick(self, event):
        OptionPageWithImports.btnRemoveModuleOnButtonClick(self, event)
