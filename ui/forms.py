# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.0.0-0-g0efcecf0)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.richtext

###########################################################################
## Class MainFrameBase
###########################################################################

class MainFrameBase ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Draw.io Code Generator", pos = wx.DefaultPosition, size = wx.Size( 1000,750 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )

        mainSizer = wx.BoxSizer( wx.VERTICAL )

        formSizer = wx.FlexGridSizer( 0, 3, 0, 0 )
        formSizer.AddGrowableCol( 1 )
        formSizer.AddGrowableRow( 2 )
        formSizer.SetFlexibleDirection( wx.BOTH )
        formSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Diagram path:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )

        formSizer.Add( self.m_staticText1, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.txtDiagramPath = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        formSizer.Add( self.txtDiagramPath, 1, wx.ALIGN_CENTER_VERTICAL|wx.BOTTOM|wx.EXPAND|wx.LEFT|wx.TOP, 5 )

        self.btnChooseDiagramPath = wx.Button( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )

        self.btnChooseDiagramPath.SetBitmap( wx.Bitmap( self.asset_path( u"assets/icons/folder.png" ), wx.BITMAP_TYPE_ANY ) )
        self.btnChooseDiagramPath.SetToolTip( u"Open a file dialog to choose the draw.io file that contains your class diagram" )

        formSizer.Add( self.btnChooseDiagramPath, 0, wx.ALIGN_CENTER_VERTICAL|wx.BOTTOM|wx.EXPAND|wx.RIGHT|wx.TOP, 5 )

        self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Output directory:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )

        formSizer.Add( self.m_staticText2, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.txtOutputPath = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        formSizer.Add( self.txtOutputPath, 1, wx.ALIGN_CENTER_VERTICAL|wx.BOTTOM|wx.EXPAND|wx.LEFT|wx.TOP, 5 )

        self.btnChooseOutputPath = wx.Button( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )

        self.btnChooseOutputPath.SetBitmap( wx.Bitmap( self.asset_path( u"assets/icons/disk.png" ), wx.BITMAP_TYPE_ANY ) )
        self.btnChooseOutputPath.SetToolTip( u"Select the folder where to store the generated files" )

        formSizer.Add( self.btnChooseOutputPath, 0, wx.ALIGN_CENTER_VERTICAL|wx.BOTTOM|wx.EXPAND|wx.RIGHT|wx.TOP, 5 )

        self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Output languages:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )

        formSizer.Add( self.m_staticText3, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        languageSizer = wx.BoxSizer( wx.HORIZONTAL )

        self.chkLangJava = wx.CheckBox( self, wx.ID_ANY, u"Java", wx.DefaultPosition, wx.DefaultSize, 0 )
        languageSizer.Add( self.chkLangJava, 0, wx.ALL, 5 )

        self.chkLangCS = wx.CheckBox( self, wx.ID_ANY, u"C#", wx.DefaultPosition, wx.DefaultSize, 0 )
        languageSizer.Add( self.chkLangCS, 0, wx.ALL, 5 )

        self.chkLangCpp = wx.CheckBox( self, wx.ID_ANY, u"C++", wx.DefaultPosition, wx.DefaultSize, 0 )
        languageSizer.Add( self.chkLangCpp, 0, wx.ALL, 5 )

        self.chkLangPython = wx.CheckBox( self, wx.ID_ANY, u"Python", wx.DefaultPosition, wx.DefaultSize, 0 )
        languageSizer.Add( self.chkLangPython, 0, wx.ALL, 5 )

        self.chkLangTS = wx.CheckBox( self, wx.ID_ANY, u"TypeScript", wx.DefaultPosition, wx.DefaultSize, 0 )
        languageSizer.Add( self.chkLangTS, 0, wx.ALL, 5 )

        self.chkLangPHP = wx.CheckBox( self, wx.ID_ANY, u"PHP", wx.DefaultPosition, wx.DefaultSize, 0 )
        languageSizer.Add( self.chkLangPHP, 0, wx.ALL, 5 )

        self.chkLangSQL = wx.CheckBox( self, wx.ID_ANY, u"SQL", wx.DefaultPosition, wx.DefaultSize, 0 )
        languageSizer.Add( self.chkLangSQL, 0, wx.ALL, 5 )


        formSizer.Add( languageSizer, 1, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )

        self.btnLangOptions = wx.Button( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )

        self.btnLangOptions.SetBitmap( wx.Bitmap( self.asset_path( u"assets/icons/setting_tools.png" ), wx.BITMAP_TYPE_ANY ) )
        self.btnLangOptions.SetToolTip( u"Configure code generation" )

        formSizer.Add( self.btnLangOptions, 0, wx.ALIGN_CENTER_VERTICAL|wx.BOTTOM|wx.EXPAND|wx.RIGHT|wx.TOP, 5 )


        mainSizer.Add( formSizer, 0, wx.EXPAND, 5 )

        treesSizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Parsing summary" ), wx.VERTICAL )

        self.nbTrees = wx.Notebook( treesSizer.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0|wx.BORDER_NONE )

        treesSizer.Add( self.nbTrees, 1, wx.EXPAND |wx.ALL, 5 )


        mainSizer.Add( treesSizer, 1, wx.ALL|wx.EXPAND, 5 )

        logSizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Log" ), wx.VERTICAL )

        logSizer.SetMinSize( wx.Size( -1,120 ) )
        self.rtcStdout = wx.richtext.RichTextCtrl( logSizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY|wx.HSCROLL|wx.VSCROLL|wx.WANTS_CHARS )
        self.rtcStdout.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.rtcStdout.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

        logSizer.Add( self.rtcStdout, 1, wx.EXPAND |wx.ALL, 5 )


        mainSizer.Add( logSizer, 0, wx.ALL|wx.EXPAND, 5 )

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


###########################################################################
## Class OptionDialogBase
###########################################################################

class OptionDialogBase ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Code Generation Options", pos = wx.DefaultPosition, size = wx.Size( 700,600 ), style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        mainSizer = wx.BoxSizer( wx.VERTICAL )

        formSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
        formSizer.AddGrowableCol( 1 )
        formSizer.SetFlexibleDirection( wx.BOTH )
        formSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"Root package name:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )

        formSizer.Add( self.m_staticText4, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.txtRootPackage = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        formSizer.Add( self.txtRootPackage, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )

        self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"Generated members:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText7.Wrap( -1 )

        formSizer.Add( self.m_staticText7, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        genMemberSizer = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

        self.chkGenerateDefaultCtor = wx.CheckBox( self, wx.ID_ANY, u"Default constructor", wx.DefaultPosition, wx.DefaultSize, 0 )
        genMemberSizer.Add( self.chkGenerateDefaultCtor, 0, wx.ALL, 5 )

        self.chkGenerateFullArgCtor = wx.CheckBox( self, wx.ID_ANY, u"Full args constructor", wx.DefaultPosition, wx.DefaultSize, 0 )
        genMemberSizer.Add( self.chkGenerateFullArgCtor, 0, wx.ALL, 5 )

        self.chkGenerateEqHc = wx.CheckBox( self, wx.ID_ANY, u"Equals and Hashcode", wx.DefaultPosition, wx.DefaultSize, 0 )
        genMemberSizer.Add( self.chkGenerateEqHc, 0, wx.ALL, 5 )

        self.chkGenerateToString = wx.CheckBox( self, wx.ID_ANY, u"ToString", wx.DefaultPosition, wx.DefaultSize, 0 )
        genMemberSizer.Add( self.chkGenerateToString, 0, wx.ALL, 5 )

        self.chkEncapsulateAllProps = wx.CheckBox( self, wx.ID_ANY, u"Make all properties private and generate public accessors", wx.DefaultPosition, wx.DefaultSize, 0 )
        genMemberSizer.Add( self.chkEncapsulateAllProps, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


        formSizer.Add( genMemberSizer, 1, wx.EXPAND, 5 )


        mainSizer.Add( formSizer, 0, wx.EXPAND, 5 )

        languageOptionsSizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Language specific options" ), wx.VERTICAL )

        self.nbLanguageOptions = wx.Notebook( languageOptionsSizer.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0|wx.BORDER_NONE )

        languageOptionsSizer.Add( self.nbLanguageOptions, 1, wx.EXPAND |wx.ALL, 5 )


        mainSizer.Add( languageOptionsSizer, 1, wx.ALL|wx.EXPAND, 5 )

        dialogButtonSizer = wx.StdDialogButtonSizer()
        self.dialogButtonSizerOK = wx.Button( self, wx.ID_OK )
        dialogButtonSizer.AddButton( self.dialogButtonSizerOK )
        self.dialogButtonSizerApply = wx.Button( self, wx.ID_APPLY )
        dialogButtonSizer.AddButton( self.dialogButtonSizerApply )
        self.dialogButtonSizerCancel = wx.Button( self, wx.ID_CANCEL )
        dialogButtonSizer.AddButton( self.dialogButtonSizerCancel )
        dialogButtonSizer.Realize();

        mainSizer.Add( dialogButtonSizer, 0, wx.ALL|wx.EXPAND, 5 )


        self.SetSizer( mainSizer )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.dialogButtonSizerApply.Bind( wx.EVT_BUTTON, self.dialogButtonSizerOnApplyButtonClick )
        self.dialogButtonSizerCancel.Bind( wx.EVT_BUTTON, self.dialogButtonSizerOnCancelButtonClick )
        self.dialogButtonSizerOK.Bind( wx.EVT_BUTTON, self.dialogButtonSizerOnOKButtonClick )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def dialogButtonSizerOnApplyButtonClick( self, event ):
        event.Skip()

    def dialogButtonSizerOnCancelButtonClick( self, event ):
        event.Skip()

    def dialogButtonSizerOnOKButtonClick( self, event ):
        event.Skip()

    # Virtual image path resolution method. Override this in your derived class.
    def asset_path( self, bitmap_path ):
        return bitmap_path


###########################################################################
## Class LanguageOptionPageBase
###########################################################################

class LanguageOptionPageBase ( wx.Panel ):

    def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,400 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
        wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

        mainSizer = wx.BoxSizer( wx.VERTICAL )

        formSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
        formSizer.AddGrowableCol( 1 )
        formSizer.SetFlexibleDirection( wx.BOTH )
        formSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.m_staticText12 = wx.StaticText( self, wx.ID_ANY, u"Module name:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText12.Wrap( -1 )

        formSizer.Add( self.m_staticText12, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.txtModuleName = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        formSizer.Add( self.txtModuleName, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )

        self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, u"Symbols to import:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText11.Wrap( -1 )

        formSizer.Add( self.m_staticText11, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.txtSymbolNames = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_WORDWRAP )
        self.txtSymbolNames.SetMinSize( wx.Size( -1,60 ) )

        formSizer.Add( self.txtSymbolNames, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )


        mainSizer.Add( formSizer, 0, wx.EXPAND, 5 )

        buttonSizer = wx.BoxSizer( wx.HORIZONTAL )


        buttonSizer.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.btnAddModule = wx.Button( self, wx.ID_ANY, u"Add to list", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.btnAddModule.SetToolTip( u"Add this module to the list of imported modules" )

        buttonSizer.Add( self.btnAddModule, 0, wx.ALL, 5 )

        self.btnRemoveModule = wx.Button( self, wx.ID_ANY, u"Remove selected", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.btnRemoveModule.SetToolTip( u"Remove the selected module from the list of imported modules" )

        buttonSizer.Add( self.btnRemoveModule, 0, wx.ALL, 5 )


        mainSizer.Add( buttonSizer, 0, wx.EXPAND, 5 )

        dividerSizer = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText141 = wx.StaticText( self, wx.ID_ANY, u"List of imported modules", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText141.Wrap( -1 )

        dividerSizer.Add( self.m_staticText141, 0, wx.ALL, 5 )

        self.m_staticline11 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        dividerSizer.Add( self.m_staticline11, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


        mainSizer.Add( dividerSizer, 0, wx.EXPAND, 5 )

        self.lstModules = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_HRULES|wx.LC_REPORT|wx.LC_SINGLE_SEL )
        mainSizer.Add( self.lstModules, 1, wx.ALL|wx.EXPAND, 5 )


        self.SetSizer( mainSizer )
        self.Layout()

        # Connect Events
        self.btnAddModule.Bind( wx.EVT_BUTTON, self.btnAddModuleOnButtonClick )
        self.btnRemoveModule.Bind( wx.EVT_BUTTON, self.btnRemoveModuleOnButtonClick )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def btnAddModuleOnButtonClick( self, event ):
        event.Skip()

    def btnRemoveModuleOnButtonClick( self, event ):
        event.Skip()

    # Virtual image path resolution method. Override this in your derived class.
    def asset_path( self, bitmap_path ):
        return bitmap_path


