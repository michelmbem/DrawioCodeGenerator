import wx

from ui.forms import LanguageOptionPageBase


class LanguageOptionPage(LanguageOptionPageBase):

    def __init__(self, parent, language, imports):
        LanguageOptionPageBase.__init__(self, parent)
        self._language = language
        self._count = 0

        self.lstModules.InsertColumn(0, "Module name", width=300)
        self.lstModules.InsertColumn(1, "Imported symbols", width=325)

        for key, value in imports.items():
            self.lstModules.InsertItem(self._count, key)
            self.lstModules.SetItem(self._count, 1, ", ".join(value))
            self._count += 1

    @property
    def language(self):
        return self._language

    @property
    def imports(self):
        _imports = {}

        for i in range(self._count):
            _imports[self.lstModules.GetItemText(i, 0)] = self.lstModules.GetItemText(i, 1).split(", ")

        return _imports

    def btnAddModuleOnButtonClick(self, event):
        self.lstModules.InsertItem(self._count, self.txtModuleName.GetValue())
        self.lstModules.SetItem(self._count, 1, self.txtSymbolNames.GetValue())
        self._count += 1

    def btnRemoveModuleOnButtonClick(self, event):
        selected_item = self.lstModules.GetFirstSelected()
        if selected_item >= 0:
            self.lstModules.DeleteItem(selected_item)
