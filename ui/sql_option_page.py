from ui.forms import SqlOptionPageBase
from ui.option_page import OptionPage


class SqlOptionPage(SqlOptionPageBase, OptionPage):

    DIALECTS = ["ansi", "mysql", "postgresql", "sqlserver", "oracle"]

    def __init__(self, parent, options):
        SqlOptionPageBase.__init__(self, parent)
        OptionPage.__init__(self)

        dialect_index = self.DIALECTS.index(options['dialect'])
        self.rbxDialect.SetSelection(dialect_index)

        if options['script_file'] == "single":
            self.rbnSingleScript.SetValue(True)
        else:
            self.rbnMultiScript.SetValue(True)

        self.txtScriptFilename.SetValue(options['filename'])
        self.onScriptRadioButtonClicked(None)

    @property
    def language(self):
        return "sql"

    @property
    def options(self):
        return {
            'dialect': self.DIALECTS[self.rbxDialect.GetSelection()],
            'script_file': "single" if self.rbnSingleScript.GetValue() else "multi",
            'filename': self.txtScriptFilename.GetValue().strip() or "database",
        }

    def asset_path(self, bitmap_path):
        return OptionPage.asset_path(self, bitmap_path)

    def onScriptRadioButtonClicked(self, event):
        self.txtScriptFilename.Enable(self.rbnSingleScript.GetValue())
