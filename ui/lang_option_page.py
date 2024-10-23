import re
import wx

from ui.forms import LanguageOptionPageBase


class LanguageOptionPage(LanguageOptionPageBase):

    LINE_COLORS = (wx.Colour(0xDDEEDD), wx.Colour(0xFFFFFF))

    def __init__(self, parent, language, options):
        LanguageOptionPageBase.__init__(self, parent)
        self._language = language
        self._count = 0

        self.lstModules.InsertColumn(0, "Module name", width=300)
        self.lstModules.InsertColumn(1, "Imported symbols", width=340)

        for module, symbols in options.get('imports', {}).items():
            self._add_import(module, symbols)

    @property
    def language(self):
        return self._language

    @property
    def options(self):
        imports = {}

        for i in range(self._count):
            module = self.lstModules.GetItemText(i, 0)
            symbols = self._split_symbol_string(self.lstModules.GetItemText(i, 1))
            imports[module] = symbols

        return {'imports': imports}

    @staticmethod
    def _split_symbol_string(string):
        return re.split(r"[\s,]+", string)

    def btnAddModuleOnButtonClick(self, event):
        module = self.txtModuleName.GetValue().strip()
        symbols = [s for s in self._split_symbol_string(self.txtSymbolNames.GetValue()) if s]

        if module:
            self._add_import(module, symbols)
        else:
            wx.MessageBox("Please supply a module name")

    def btnRemoveModuleOnButtonClick(self, event):
        selected_index = self.lstModules.GetFirstSelected()
        if selected_index >= 0:
            self._remove_import(selected_index)
            if self._count > selected_index:
                self.lstModules.Select(selected_index)
        else:
            wx.MessageBox("There is no selection in the list")

    def _add_import(self, module, symbols):
        self.lstModules.InsertItem(self._count, module)
        self.lstModules.SetItem(self._count, 1, ', '.join(symbols or []))
        self.lstModules.SetItemBackgroundColour(self._count, self.LINE_COLORS[self._count % 2])
        self._count += 1

    def _remove_import(self, index):
        self.lstModules.DeleteItem(index)
        self._count -= 1

        for row_index in range(index, self._count):
            self.lstModules.SetItemBackgroundColour(row_index, self.LINE_COLORS[row_index % 2])
