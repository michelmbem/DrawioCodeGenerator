from ui.forms import JavaOptionPageBase
from ui.option_page_with_import import OptionPageWithImports


class JavaOptionPage(JavaOptionPageBase, OptionPageWithImports):

    TEMPORAL_TYPES = ["java8_local", "java8_offset", "sql_date", "util_date", "calendar"]

    def __init__(self, parent, options):
        JavaOptionPageBase.__init__(self, parent)
        OptionPageWithImports.__init__(self, "java", options)

        self.chkUseLombok.SetValue(options['use_lombok'])
        self.chkUseLombokOnCheckBox(None)
        self.chkAddBuilderAnno.SetValue(options['add_builder'])
        self.chkAddJpaAnno.SetValue(options['add_jpa'])
        self.chcTemporal.SetSelection(self.TEMPORAL_TYPES.index(options['temporal_types']))

        if options['use_jakarta']:
            self.rbnJeeRootJakarta.SetValue(True)
        else:
            self.rbnJeeRootJavax.SetValue(True)

    @property
    def options(self):
        return {
            'use_lombok': self.chkUseLombok.IsChecked(),
            'add_builder': self.chkAddBuilderAnno.IsChecked(),
            'add_jpa': self.chkAddJpaAnno.IsChecked(),
            'use_jakarta': self.rbnJeeRootJakarta.GetValue(),
            'temporal_types': self.TEMPORAL_TYPES[self.chcTemporal.GetSelection()],
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

    def btnAddImportOnButtonClick(self, event):
        OptionPageWithImports.btnAddImportOnButtonClick(self, event)

    def btnUpdateImportOnButtonClick( self, event ):
        OptionPageWithImports.btnUpdateImportOnButtonClick(self, event)

    def btnRemoveImportOnButtonClick(self, event):
        OptionPageWithImports.btnRemoveImportOnButtonClick(self, event)
