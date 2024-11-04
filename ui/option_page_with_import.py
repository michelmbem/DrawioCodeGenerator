import re
from lib2to3.pygram import Symbols
from modulefinder import Module

import wx

from ui.platform import OPTION_DLG_SIZE
from ui.option_page import OptionPage


class OptionPageWithImports(OptionPage):

    LABELS = {
        'php': {'module_name': "Required script:"},
    }

    def __init__(self, language, options):
        super().__init__()
        self._language = language

        labels = self.LABELS.get(language)
        if labels:
            self.lblModuleName.SetLabel(labels['module_name'])
            if 'symbol_names' in labels:
                self.lblSymbolNames.SetLabel(labels['symbol_names'])

        if language in ("cs", "cpp", "php"):
            self.lblSymbolNames.Hide()
            self.txtSymbolNames.Hide()

        self.lscImport.InsertColumn(0, self.lblModuleName.GetLabel()[:-1])
        self.lscImport.InsertColumn(1, self.lblSymbolNames.GetLabel()[:-1])

        dlg_width = OPTION_DLG_SIZE[0] - 90
        if self.lblSymbolNames.Shown:
            self.lscImport.SetColumnWidth(0, int(.4 * dlg_width))
            self.lscImport.SetColumnWidth(1, int(.6 * dlg_width))
        else:
            self.lscImport.SetColumnWidth(0, dlg_width)
            self.lscImport.SetColumnWidth(1, 0)

        for module, symbols in options.get('imports', {}).items():
            self.add_import(module, symbols)

        self.lscImportOnListItemSelected(None)

    @property
    def language(self):
        return self._language

    @property
    def options(self):
        imports = {}

        for i in range(self.lscImport.GetItemCount()):
            module = self.lscImport.GetItemText(i, 0)
            symbols = self.split_symbol_string(self.lscImport.GetItemText(i, 1))
            imports[module] = symbols

        return {'imports': imports}

    @staticmethod
    def split_symbol_string(string):
        return re.split(r"[\s,]+", string)

    def get_user_input(self):
        module = self.txtModuleName.GetValue().strip()
        symbols = [s for s in self.split_symbol_string(self.txtSymbolNames.GetValue()) if s]
        return module, symbols

    def show_validation_message(self):
        module_name = self.lscImport.GetColumn(0).GetText().lower()
        wx.MessageBox(f"Please supply a {module_name}", "Invalid input", wx.OK | wx.ICON_WARNING)

    def show_selection_message(self):
        wx.MessageBox("There was no selection in the list", "Invalid input", wx.OK | wx.ICON_WARNING)

    def add_import(self, module, symbols):
        new_index = self.lscImport.GetItemCount()
        self.lscImport.InsertItem(new_index, module)
        self.lscImport.SetItem(new_index, 1, ', '.join(symbols or []))
        self.lscImport.SetItemBackgroundColour(new_index, self.line_colors[new_index % 2])

    def update_import(self, index, module, symbols):
        self.lscImport.SetItem(index, 0, module)
        self.lscImport.SetItem(index, 1, ', '.join(symbols))

    def remove_import(self, index):
        self.lscImport.DeleteItem(index)

        for row_index in range(index, self.lscImport.GetItemCount()):
            self.lscImport.SetItemBackgroundColour(row_index, self.line_colors[row_index % 2])

    def lscImportOnListItemSelected(self, event):
        selected_index = self.lscImport.GetFirstSelected()

        if selected_index >= 0:
            self.txtModuleName.SetValue(self.lscImport.GetItemText(selected_index, 0))
            self.txtSymbolNames.SetValue(self.lscImport.GetItemText(selected_index, 1))
            self.btnUpdateImport.Enable(True)
            self.btnRemoveImport.Enable(True)
        else:
            self.txtModuleName.Clear()
            self.txtSymbolNames.Clear()
            self.btnUpdateImport.Enable(False)
            self.btnRemoveImport.Enable(False)

    def btnAddImportOnButtonClick(self, event):
        module, symbols = self.get_user_input()

        if module:
            self.add_import(module, symbols)
        else:
            self.show_validation_message()

    def btnUpdateImportOnButtonClick( self, event ):
        selected_index = self.lscImport.GetFirstSelected()

        if selected_index >= 0:
            module, symbols = self.get_user_input()

            if module:
                self.update_import(selected_index, module, symbols)
            else:
                self.show_validation_message()
        else:
            self.show_selection_message()

    def btnRemoveImportOnButtonClick(self, event):
        selected_index = self.lscImport.GetFirstSelected()

        if selected_index >= 0:
            self.remove_import(selected_index)
            line_count = self.lscImport.GetItemCount()

            if line_count > selected_index:
                self.lscImport.Select(selected_index)
            elif line_count > 0:
                self.lscImport.Select(line_count - 1)
        else:
            self.show_selection_message()
