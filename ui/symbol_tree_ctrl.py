import wx
import wx.lib.gizmos as gizmos


class SymbolTreeCtrl(gizmos.TreeListCtrl):

    def __init__(self, parent):
        super().__init__(parent, agwStyle=gizmos.TR_DEFAULT_STYLE | gizmos.TR_HIDE_ROOT |
                                          gizmos.TR_ROW_LINES | gizmos.TR_FULL_ROW_HIGHLIGHT)

        image_size = (16, 16)
        image_list = wx.ImageList(*image_size)
        self.folder_img_ndx = image_list.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, image_size))
        self.folder_open_img_ndx = image_list.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, image_size))
        self.file_img_ndx = image_list.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, image_size))
        self.SetImageList(image_list)

        total_width = self.GetParent().GetClientSize().width - 30
        self.AddColumn("Attribute name", width=int(.33 * total_width))
        self.AddColumn("Attribue value", width=int(.67 * total_width))
        self.SetMainColumn(0)

    def load_dict(self, dictionary):
        self.DeleteAllItems()
        if dictionary:
            self.create_nodes_from_dict(self.AddRoot("#"), dictionary)
            self.ExpandAll()

    def create_nodes_from_dict(self, parent_node, dictionary):
        for key, value in dictionary.items():
            child_node = self.AppendItem(parent_node, str(key))

            if isinstance(value, dict):
                self.SetItemImage(child_node, self.folder_img_ndx, wx.TreeItemIcon_Normal)
                self.SetItemImage(child_node, self.folder_open_img_ndx, wx.TreeItemIcon_Expanded)
                self.create_nodes_from_dict(child_node, value)
            else:
                self.SetItemText(child_node, str(value), 1)
                self.SetItemImage(child_node, self.file_img_ndx, wx.TreeItemIcon_Normal)
