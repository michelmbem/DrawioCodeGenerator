import re
import wx

from ui.platform import OPTION_DLG_SIZE
from ui.forms import LanguageOptionPageBase


class LanguageOptionPage(LanguageOptionPageBase):

    def __init__(self, parent, language, options):
        super().__init__(parent)
        self.language = language
        self.line_count = 0

        if wx.SystemSettings.GetAppearance().IsUsingDarkBackground():
            self.line_colors = (wx.Colour(0x334433), wx.Colour(0x222222))
        else:
            self.line_colors = (wx.Colour(0xDDEEDD), wx.Colour(0xFFFFFF))

        dlg_width = OPTION_DLG_SIZE[0] - 80
        self.lstModules.InsertColumn(0, "Module name", width=int(.4 * dlg_width))
        self.lstModules.InsertColumn(1, "Imported symbols", width=int(.6 * dlg_width))

        for module, symbols in options.get('imports', {}).items():
            self.add_import(module, symbols)

        if language in ("cs", "cpp", "php"):
            self.txtSymbolNames.Enable(False)

    @property
    def options(self):
        imports = {}

        for i in range(self.line_count):
            module = self.lstModules.GetItemText(i, 0)
            symbols = self.split_symbol_string(self.lstModules.GetItemText(i, 1))
            imports[module] = symbols

        return {'imports': imports}

    @staticmethod
    def split_symbol_string(string):
        return re.split(r"[\s,]+", string)

    def add_import(self, module, symbols):
        self.lstModules.InsertItem(self.line_count, module)
        self.lstModules.SetItem(self.line_count, 1, ', '.join(symbols or []))
        self.lstModules.SetItemBackgroundColour(self.line_count, self.line_colors[self.line_count % 2])
        self.line_count += 1

    def remove_import(self, index):
        self.lstModules.DeleteItem(index)
        self.line_count -= 1

        for row_index in range(index, self.line_count):
            self.lstModules.SetItemBackgroundColour(row_index, self.line_colors[row_index % 2])

    def btnAddModuleOnButtonClick(self, event):
        module = self.txtModuleName.GetValue().strip()
        symbols = [s for s in self.split_symbol_string(self.txtSymbolNames.GetValue()) if s]

        if module:
            self.add_import(module, symbols)
        else:
            wx.MessageBox("Please supply a module name")

    def btnRemoveModuleOnButtonClick(self, event):
        selected_index = self.lstModules.GetFirstSelected()
        if selected_index >= 0:
            self.remove_import(selected_index)
            if self.line_count > selected_index:
                self.lstModules.Select(selected_index)
            else:
                self.lstModules.Select(self.lstModules.GetItemCount() - 1)
        else:
            wx.MessageBox("There is no selection in the list")
