import re
import wx

from ui.platform import OPTION_DLG_SIZE
from ui.option_page import OptionPage


class OptionPageWithImports(OptionPage):

    LABELS = {
        'cpp': {'module_name': "Header file", 'symbol_names': "Elements to import"},
    }

    def __init__(self, language, options):
        super().__init__()
        self._language = language

        labels = self.LABELS.get(language)
        if labels:
            self.lblModuleName.SetLabel(labels['module_name'] + ':')
            self.lblSymbolNames.SetLabel(labels['symbol_names'] + ':')

        if language in ("cs", "cpp", "php"):
            self.txtSymbolNames.SetValue("[All]")
            self.txtSymbolNames.Enable(False)

        dlg_width = OPTION_DLG_SIZE[0] - 80
        self.lstModules.InsertColumn(0, self.lblModuleName.GetLabel()[:-1], width=int(.4 * dlg_width))
        self.lstModules.InsertColumn(1, self.lblSymbolNames.GetLabel()[:-1], width=int(.6 * dlg_width))

        for module, symbols in options.get('imports', {}).items():
            self.add_import(module, symbols)

    @property
    def language(self):
        return self._language

    @property
    def options(self):
        imports = {}

        for i in range(self.lstModules.GetItemCount()):
            module = self.lstModules.GetItemText(i, 0)
            symbols = self.split_symbol_string(self.lstModules.GetItemText(i, 1))
            imports[module] = symbols

        return {'imports': imports}

    @staticmethod
    def split_symbol_string(string):
        return re.split(r"[\s,]+", string)

    def add_import(self, module, symbols):
        new_index = self.lstModules.GetItemCount()
        self.lstModules.InsertItem(new_index, module)
        self.lstModules.SetItem(new_index, 1, ', '.join(symbols or []))
        self.lstModules.SetItemBackgroundColour(new_index, self.line_colors[new_index % 2])

    def remove_import(self, index):
        self.lstModules.DeleteItem(index)

        for row_index in range(index, self.lstModules.GetItemCount()):
            self.lstModules.SetItemBackgroundColour(row_index, self.line_colors[row_index % 2])

    def btnAddModuleOnButtonClick(self, event):
        module = self.txtModuleName.GetValue().strip()
        symbols = [s for s in self.split_symbol_string(self.txtSymbolNames.GetValue()) if s]

        if module:
            self.add_import(module, symbols)
        else:
            module_name = self.lstModules.GetColumn(0).GetText().lower()
            wx.MessageBox(f"Please supply a {module_name}", "Invalid input", wx.OK | wx.ICON_WARNING)

    def btnRemoveModuleOnButtonClick(self, event):
        selected_index = self.lstModules.GetFirstSelected()

        if selected_index >= 0:
            self.remove_import(selected_index)
            line_count = self.lstModules.GetItemCount()

            if line_count > selected_index:
                self.lstModules.Select(selected_index)
            elif line_count > 0:
                self.lstModules.Select(line_count - 1)
        else:
            wx.MessageBox("There is no selection in the list", "Invalid input", wx.OK | wx.ICON_WARNING)
