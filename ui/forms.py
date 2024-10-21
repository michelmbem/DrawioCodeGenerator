# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.0.0-0-g0efcecf)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MainFrameBase
###########################################################################

class MainFrameBase ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Draw.io Code Generator", pos = wx.DefaultPosition, size = wx.Size( 800,600 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )

        mainSizer = wx.BoxSizer( wx.VERTICAL )

        formSizer = wx.FlexGridSizer( 3, 3, 0, 0 )
        formSizer.AddGrowableCol( 1 )
        formSizer.AddGrowableRow( 2 )
        formSizer.SetFlexibleDirection( wx.BOTH )
        formSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Dragram path:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )

        formSizer.Add( self.m_staticText1, 0, wx.ALL, 5 )

        self.txtDiagramPath = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        formSizer.Add( self.txtDiagramPath, 1, wx.ALL|wx.EXPAND, 5 )

        self.btnChooseDiagramPath = wx.Button( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )

        self.btnChooseDiagramPath.SetBitmap( wx.Bitmap( self.asset_path( u"assets/icons/folder.png" ), wx.BITMAP_TYPE_ANY ) )
        self.btnChooseDiagramPath.SetToolTip( u"Choose a file" )

        formSizer.Add( self.btnChooseDiagramPath, 0, wx.ALL, 5 )

        self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Output path:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )

        formSizer.Add( self.m_staticText2, 0, wx.ALL, 5 )

        self.txtOutputPath = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        formSizer.Add( self.txtOutputPath, 1, wx.ALL|wx.EXPAND, 5 )

        self.btnChooseOutputPath = wx.Button( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )

        self.btnChooseOutputPath.SetBitmap( wx.Bitmap( self.asset_path( u"assets/icons/disk.png" ), wx.BITMAP_TYPE_ANY ) )
        self.btnChooseOutputPath.SetToolTip( u"Choose a folder" )

        formSizer.Add( self.btnChooseOutputPath, 0, wx.ALL, 5 )

        self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Output languages:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )

        formSizer.Add( self.m_staticText3, 0, wx.ALL, 5 )

        languageSizer = wx.BoxSizer( wx.HORIZONTAL )

        self.chkLangTS = wx.CheckBox( self, wx.ID_ANY, u"TypeScript", wx.DefaultPosition, wx.DefaultSize, 0 )
        languageSizer.Add( self.chkLangTS, 0, wx.ALL, 5 )

        self.chkLangJava = wx.CheckBox( self, wx.ID_ANY, u"Java", wx.DefaultPosition, wx.DefaultSize, 0 )
        languageSizer.Add( self.chkLangJava, 0, wx.ALL, 5 )

        self.chkLangCS = wx.CheckBox( self, wx.ID_ANY, u"C#", wx.DefaultPosition, wx.DefaultSize, 0 )
        languageSizer.Add( self.chkLangCS, 0, wx.ALL, 5 )

        self.chkLangCpp = wx.CheckBox( self, wx.ID_ANY, u"C++", wx.DefaultPosition, wx.DefaultSize, 0 )
        languageSizer.Add( self.chkLangCpp, 0, wx.ALL, 5 )

        self.chkLangPHP = wx.CheckBox( self, wx.ID_ANY, u"PHP", wx.DefaultPosition, wx.DefaultSize, 0 )
        languageSizer.Add( self.chkLangPHP, 0, wx.ALL, 5 )

        self.chkLangPython = wx.CheckBox( self, wx.ID_ANY, u"Python", wx.DefaultPosition, wx.DefaultSize, 0 )
        languageSizer.Add( self.chkLangPython, 0, wx.ALL, 5 )

        self.chkLangSQL = wx.CheckBox( self, wx.ID_ANY, u"SQL", wx.DefaultPosition, wx.DefaultSize, 0 )
        languageSizer.Add( self.chkLangSQL, 0, wx.ALL, 5 )


        formSizer.Add( languageSizer, 1, wx.EXPAND, 5 )

        self.btnLangOptions = wx.Button( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )

        self.btnLangOptions.SetBitmap( wx.Bitmap( self.asset_path( u"assets/icons/setting_tools.png" ), wx.BITMAP_TYPE_ANY ) )
        self.btnLangOptions.SetToolTip( u"Configure code generation" )

        formSizer.Add( self.btnLangOptions, 0, wx.ALL, 5 )


        mainSizer.Add( formSizer, 0, wx.EXPAND, 5 )

        treesSizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Parsing summary" ), wx.VERTICAL )

        self.nbTrees = wx.Notebook( treesSizer.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

        treesSizer.Add( self.nbTrees, 1, wx.EXPAND |wx.ALL, 5 )


        mainSizer.Add( treesSizer, 1, wx.EXPAND, 5 )

        buttonSizer = wx.BoxSizer( wx.HORIZONTAL )


        buttonSizer.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.btnGenerate = wx.Button( self, wx.ID_ANY, u"Generate", wx.DefaultPosition, wx.DefaultSize, 0 )

        self.btnGenerate.SetDefault()

        self.btnGenerate.SetBitmap( wx.Bitmap( self.asset_path( u"assets/icons/lightning.png" ), wx.BITMAP_TYPE_ANY ) )
        self.btnGenerate.SetToolTip( u"Generate code" )

        buttonSizer.Add( self.btnGenerate, 0, wx.ALL, 5 )

        self.btnExit = wx.Button( self, wx.ID_ANY, u"Exit", wx.DefaultPosition, wx.DefaultSize, 0 )

        self.btnExit.SetBitmap( wx.Bitmap( self.asset_path( u"assets/icons/door_in.png" ), wx.BITMAP_TYPE_ANY ) )
        self.btnExit.SetToolTip( u"Exit this application" )

        buttonSizer.Add( self.btnExit, 0, wx.ALL, 5 )


        mainSizer.Add( buttonSizer, 0, wx.EXPAND, 5 )


        self.SetSizer( mainSizer )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.btnChooseDiagramPath.Bind( wx.EVT_BUTTON, self.btnChooseDiagramPathOnButtonClick )
        self.btnChooseOutputPath.Bind( wx.EVT_BUTTON, self.btnChooseOutputPathOnButtonClick )
        self.btnLangOptions.Bind( wx.EVT_BUTTON, self.btnLangOptionsOnButtonClick )
        self.btnGenerate.Bind( wx.EVT_BUTTON, self.btnGenerateOnButtonClick )
        self.btnExit.Bind( wx.EVT_BUTTON, self.btnExitOnButtonClick )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def btnChooseDiagramPathOnButtonClick( self, event ):
        event.Skip()

    def btnChooseOutputPathOnButtonClick( self, event ):
        event.Skip()

    def btnLangOptionsOnButtonClick( self, event ):
        event.Skip()

    def btnGenerateOnButtonClick( self, event ):
        event.Skip()

    def btnExitOnButtonClick( self, event ):
        event.Skip()

    # Virtual image path resolution method. Override this in your derived class.
    def asset_path( self, bitmap_path ):
        return bitmap_path


