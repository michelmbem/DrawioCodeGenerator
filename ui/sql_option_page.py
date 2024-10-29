from ui.forms import SqlOptionPageBase
from ui.option_page import OptionPage


class SqlOptionPage(SqlOptionPageBase, OptionPage):

    DIALECTS = ["ansi", "mysql", "postgresql", "sqlserver", "oracle"]

    def __init__(self, parent, options):
        SqlOptionPageBase.__init__(self, parent)
        OptionPage.__init__(self)

        dialect_index = self.DIALECTS.index(options.get('dialect', "ansi"))
        self.rbxDialect.SetSelection(dialect_index)

    @property
    def language(self):
        return "sql"

    @property
    def options(self):
        return {'dialect': self.DIALECTS[self.rbxDialect.GetSelection()]}
