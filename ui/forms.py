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

        formSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
        formSizer.AddGrowableCol( 1 )
        formSizer.SetFlexibleDirection( wx.BOTH )
        formSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Diagram path:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )

        formSizer.Add( self.m_staticText1, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.fpcDiagramPath = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Open a diagram", u"Draw.io diagram files (*.drawio)|*.drawio|All files (*.*)|*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE|wx.FLP_USE_TEXTCTRL )
        self.fpcDiagramPath.SetToolTip( u"Open a file dialog and browse to choose a draw.io class diagram file" )

        formSizer.Add( self.fpcDiagramPath, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )

        self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Output directory:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )

        formSizer.Add( self.m_staticText2, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.dpcOutputDir = wx.DirPickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select output directory", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE|wx.DIRP_USE_TEXTCTRL )
        self.dpcOutputDir.SetToolTip( u"Select the directory where to store generated code files" )

        formSizer.Add( self.dpcOutputDir, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Output languages:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )

        formSizer.Add( self.m_staticText3, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        languageSizer = wx.BoxSizer( wx.HORIZONTAL )

        self.chkLangJava = wx.CheckBox( self, wx.ID_ANY, u"Java", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.chkLangJava.SetToolTip( u"Check to generate Java source code" )

        languageSizer.Add( self.chkLangJava, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.chkLangCS = wx.CheckBox( self, wx.ID_ANY, u"C#", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.chkLangCS.SetToolTip( u"Check to generate C# source code" )

        languageSizer.Add( self.chkLangCS, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.chkLangCpp = wx.CheckBox( self, wx.ID_ANY, u"C++", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.chkLangCpp.SetToolTip( u"Check to generate C++ source code" )

        languageSizer.Add( self.chkLangCpp, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.chkLangPython = wx.CheckBox( self, wx.ID_ANY, u"Python", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.chkLangPython.SetToolTip( u"Check to generate Python source code" )

        languageSizer.Add( self.chkLangPython, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.chkLangTS = wx.CheckBox( self, wx.ID_ANY, u"TypeScript", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.chkLangTS.SetToolTip( u"Check to generate TypeScript source code" )

        languageSizer.Add( self.chkLangTS, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.chkLangPHP = wx.CheckBox( self, wx.ID_ANY, u"PHP", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.chkLangPHP.SetToolTip( u"Check to generate PHP source code" )

        languageSizer.Add( self.chkLangPHP, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.chkLangSQL = wx.CheckBox( self, wx.ID_ANY, u"SQL", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.chkLangSQL.SetToolTip( u"Check to generate SQL source code" )

        languageSizer.Add( self.chkLangSQL, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


        languageSizer.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.btnLangOptions = wx.Button( self, wx.ID_ANY, u"More options", wx.DefaultPosition, wx.DefaultSize, 0 )

        self.btnLangOptions.SetBitmap( wx.Bitmap( self.asset_path( u"assets/icons/setting_tools.png" ), wx.BITMAP_TYPE_ANY ) )
        self.btnLangOptions.SetToolTip( u"Open a dialog to configure additional code generation options" )

        languageSizer.Add( self.btnLangOptions, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


        formSizer.Add( languageSizer, 1, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )


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

        self.btnParse = wx.Button( self, wx.ID_ANY, u"Parse", wx.DefaultPosition, wx.DefaultSize, 0 )

        self.btnParse.SetBitmap( wx.Bitmap( self.asset_path( u"assets/icons/page_white_magnify.png" ), wx.BITMAP_TYPE_ANY ) )
        self.btnParse.SetToolTip( u"Parse the diagram in preparation for code generation" )

        buttonSizer.Add( self.btnParse, 0, wx.ALL, 5 )

        self.btnGenerate = wx.Button( self, wx.ID_ANY, u"Generate", wx.DefaultPosition, wx.DefaultSize, 0 )

        self.btnGenerate.SetDefault()

        self.btnGenerate.SetBitmap( wx.Bitmap( self.asset_path( u"assets/icons/lightning.png" ), wx.BITMAP_TYPE_ANY ) )
        self.btnGenerate.SetToolTip( u"Generate code from the selected diagram" )

        buttonSizer.Add( self.btnGenerate, 0, wx.ALL, 5 )

        self.m_staticline2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
        buttonSizer.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )

        self.btnExit = wx.Button( self, wx.ID_ANY, u"Exit", wx.DefaultPosition, wx.DefaultSize, 0 )

        self.btnExit.SetBitmap( wx.Bitmap( self.asset_path( u"assets/icons/door_in.png" ), wx.BITMAP_TYPE_ANY ) )
        self.btnExit.SetToolTip( u"Exit this application" )

        buttonSizer.Add( self.btnExit, 0, wx.ALL, 5 )


        mainSizer.Add( buttonSizer, 0, wx.EXPAND, 5 )


        self.SetSizer( mainSizer )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.fpcDiagramPath.Bind( wx.EVT_FILEPICKER_CHANGED, self.fpcDiagramPathOnFileChanged )
        self.btnLangOptions.Bind( wx.EVT_BUTTON, self.btnLangOptionsOnButtonClick )
        self.btnParse.Bind( wx.EVT_BUTTON, self.btnParseOnButtonClick )
        self.btnGenerate.Bind( wx.EVT_BUTTON, self.btnGenerateOnButtonClick )
        self.btnExit.Bind( wx.EVT_BUTTON, self.btnExitOnButtonClick )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def fpcDiagramPathOnFileChanged( self, event ):
        event.Skip()

    def btnLangOptionsOnButtonClick( self, event ):
        event.Skip()

    def btnParseOnButtonClick( self, event ):
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
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Code Generation Options", pos = wx.DefaultPosition, size = wx.Size( 700,625 ), style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        mainSizer = wx.BoxSizer( wx.VERTICAL )

        commonOptionsSizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Common options" ), wx.VERTICAL )

        formSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
        formSizer.AddGrowableCol( 1 )
        formSizer.SetFlexibleDirection( wx.BOTH )
        formSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.m_staticText4 = wx.StaticText( commonOptionsSizer.GetStaticBox(), wx.ID_ANY, u"Root package name:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )

        formSizer.Add( self.m_staticText4, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.txtRootPackage = wx.TextCtrl( commonOptionsSizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        formSizer.Add( self.txtRootPackage, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )

        self.m_staticText7 = wx.StaticText( commonOptionsSizer.GetStaticBox(), wx.ID_ANY, u"Generated members:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText7.Wrap( -1 )

        formSizer.Add( self.m_staticText7, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        genMemberSizer = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )

        self.chkGenerateDefaultCtor = wx.CheckBox( commonOptionsSizer.GetStaticBox(), wx.ID_ANY, u"Default constructor", wx.DefaultPosition, wx.DefaultSize, 0 )
        genMemberSizer.Add( self.chkGenerateDefaultCtor, 0, wx.ALL, 5 )

        self.chkGenerateFullArgCtor = wx.CheckBox( commonOptionsSizer.GetStaticBox(), wx.ID_ANY, u"Full args constructor", wx.DefaultPosition, wx.DefaultSize, 0 )
        genMemberSizer.Add( self.chkGenerateFullArgCtor, 0, wx.ALL, 5 )

        self.chkGenerateEqHc = wx.CheckBox( commonOptionsSizer.GetStaticBox(), wx.ID_ANY, u"Equals and HashCode", wx.DefaultPosition, wx.DefaultSize, 0 )
        genMemberSizer.Add( self.chkGenerateEqHc, 0, wx.ALL, 5 )

        self.chkGenerateToString = wx.CheckBox( commonOptionsSizer.GetStaticBox(), wx.ID_ANY, u"ToString", wx.DefaultPosition, wx.DefaultSize, 0 )
        genMemberSizer.Add( self.chkGenerateToString, 0, wx.ALL, 5 )

        self.chkEncapsulateAllProps = wx.CheckBox( commonOptionsSizer.GetStaticBox(), wx.ID_ANY, u"Make all properties private and generate public accessors", wx.DefaultPosition, wx.DefaultSize, 0 )
        genMemberSizer.Add( self.chkEncapsulateAllProps, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


        formSizer.Add( genMemberSizer, 1, wx.EXPAND, 5 )


        commonOptionsSizer.Add( formSizer, 0, wx.EXPAND, 5 )


        mainSizer.Add( commonOptionsSizer, 0, wx.ALL|wx.EXPAND, 5 )

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
## Class CommonOptionPageBase
###########################################################################

class CommonOptionPageBase ( wx.Panel ):

    def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,400 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
        wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

        mainSizer = wx.BoxSizer( wx.VERTICAL )

        importSizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Imports" ), wx.VERTICAL )

        self.lscImport = wx.ListCtrl( importSizer.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_HRULES|wx.LC_REPORT|wx.LC_SINGLE_SEL )
        importSizer.Add( self.lscImport, 1, wx.ALL|wx.EXPAND, 5 )

        formSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
        formSizer.AddGrowableCol( 1 )
        formSizer.SetFlexibleDirection( wx.BOTH )
        formSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.lblModuleName = wx.StaticText( importSizer.GetStaticBox(), wx.ID_ANY, u"Module name:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.lblModuleName.Wrap( -1 )

        formSizer.Add( self.lblModuleName, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.txtModuleName = wx.TextCtrl( importSizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.txtModuleName.SetToolTip( u"Type in the name of a module/header file that should be automatically imported/included in each generated code file" )

        formSizer.Add( self.txtModuleName, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )

        self.lblSymbolNames = wx.StaticText( importSizer.GetStaticBox(), wx.ID_ANY, u"Symbols to import:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.lblSymbolNames.Wrap( -1 )

        formSizer.Add( self.lblSymbolNames, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.txtSymbolNames = wx.TextCtrl( importSizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_WORDWRAP )
        self.txtSymbolNames.SetToolTip( u"Type in the names of types, constants  and/or functions that should be imported from the above module in each generated code file.\nSeparate the names with spaces or commas" )
        self.txtSymbolNames.SetMinSize( wx.Size( -1,60 ) )

        formSizer.Add( self.txtSymbolNames, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )


        importSizer.Add( formSizer, 0, wx.EXPAND, 5 )

        buttonSizer = wx.BoxSizer( wx.HORIZONTAL )


        buttonSizer.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.btnAddImport = wx.Button( importSizer.GetStaticBox(), wx.ID_ANY, u"Add to list", wx.DefaultPosition, wx.DefaultSize, 0 )

        self.btnAddImport.SetBitmap( wx.Bitmap( self.asset_path( u"assets/icons/add.png" ), wx.BITMAP_TYPE_ANY ) )
        self.btnAddImport.SetToolTip( u"Add the above definition to the list of imports" )

        buttonSizer.Add( self.btnAddImport, 0, wx.ALL, 5 )

        self.btnUpdateImport = wx.Button( importSizer.GetStaticBox(), wx.ID_ANY, u"Update", wx.DefaultPosition, wx.DefaultSize, 0 )

        self.btnUpdateImport.SetBitmap( wx.Bitmap( self.asset_path( u"assets/icons/accept.png" ), wx.BITMAP_TYPE_ANY ) )
        self.btnUpdateImport.SetToolTip( u"Update the selected import" )

        buttonSizer.Add( self.btnUpdateImport, 0, wx.ALL, 5 )

        self.btnRemoveImport = wx.Button( importSizer.GetStaticBox(), wx.ID_ANY, u"Remove selected", wx.DefaultPosition, wx.DefaultSize, 0 )

        self.btnRemoveImport.SetBitmap( wx.Bitmap( self.asset_path( u"assets/icons/delete.png" ), wx.BITMAP_TYPE_ANY ) )
        self.btnRemoveImport.SetToolTip( u"Remove the selected import from the list" )

        buttonSizer.Add( self.btnRemoveImport, 0, wx.ALL, 5 )


        importSizer.Add( buttonSizer, 0, wx.EXPAND, 5 )


        mainSizer.Add( importSizer, 1, wx.ALL|wx.EXPAND, 5 )


        self.SetSizer( mainSizer )
        self.Layout()

        # Connect Events
        self.lscImport.Bind( wx.EVT_LIST_ITEM_SELECTED, self.lscImportOnListItemSelected )
        self.btnAddImport.Bind( wx.EVT_BUTTON, self.btnAddImportOnButtonClick )
        self.btnUpdateImport.Bind( wx.EVT_BUTTON, self.btnUpdateImportOnButtonClick )
        self.btnRemoveImport.Bind( wx.EVT_BUTTON, self.btnRemoveImportOnButtonClick )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def lscImportOnListItemSelected( self, event ):
        event.Skip()

    def btnAddImportOnButtonClick( self, event ):
        event.Skip()

    def btnUpdateImportOnButtonClick( self, event ):
        event.Skip()

    def btnRemoveImportOnButtonClick( self, event ):
        event.Skip()

    # Virtual image path resolution method. Override this in your derived class.
    def asset_path( self, bitmap_path ):
        return bitmap_path


###########################################################################
## Class JavaOptionPageBase
###########################################################################

class JavaOptionPageBase ( wx.Panel ):

    def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,400 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
        wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

        mainSizer = wx.BoxSizer( wx.VERTICAL )

        featuresSizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Additional features" ), wx.VERTICAL )

        checkBoxSizer = wx.BoxSizer( wx.HORIZONTAL )

        self.chkUseLombok = wx.CheckBox( featuresSizer.GetStaticBox(), wx.ID_ANY, u"Use lombok annotations", wx.DefaultPosition, wx.DefaultSize, 0 )
        checkBoxSizer.Add( self.chkUseLombok, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.chkAddBuilderAnno = wx.CheckBox( featuresSizer.GetStaticBox(), wx.ID_ANY, u"Add @Builder annotation", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.chkAddBuilderAnno.Enable( False )

        checkBoxSizer.Add( self.chkAddBuilderAnno, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.chkAddJpaAnno = wx.CheckBox( featuresSizer.GetStaticBox(), wx.ID_ANY, u"Add JPA data annotations", wx.DefaultPosition, wx.DefaultSize, 0 )
        checkBoxSizer.Add( self.chkAddJpaAnno, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


        featuresSizer.Add( checkBoxSizer, 0, wx.EXPAND, 5 )

        featureFormSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
        featureFormSizer.AddGrowableCol( 1 )
        featureFormSizer.SetFlexibleDirection( wx.BOTH )
        featureFormSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.m_staticText12 = wx.StaticText( featuresSizer.GetStaticBox(), wx.ID_ANY, u"Map temporal types to:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText12.Wrap( -1 )

        featureFormSizer.Add( self.m_staticText12, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        chcTemporalChoices = [ u"Java 8 local time: LocalDate, LocalTime and LocalDateTime", u"Java 8 time with offset: LocalDate, OffsetTime and OffsetDateTime", u"JDBC (java.sql): Date, Time and Timestamp", u"java.util.Date", u"java.util.Calendar" ]
        self.chcTemporal = wx.Choice( featuresSizer.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, chcTemporalChoices, 0 )
        self.chcTemporal.SetSelection( 0 )
        featureFormSizer.Add( self.chcTemporal, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )

        self.m_staticText13 = wx.StaticText( featuresSizer.GetStaticBox(), wx.ID_ANY, u"JEE root package name:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText13.Wrap( -1 )

        featureFormSizer.Add( self.m_staticText13, 0, wx.ALL, 5 )

        jeeRootPkgSizer = wx.BoxSizer( wx.HORIZONTAL )

        self.rbnJeeRootJavax = wx.RadioButton( featuresSizer.GetStaticBox(), wx.ID_ANY, u"javax", wx.DefaultPosition, wx.DefaultSize, 0 )
        jeeRootPkgSizer.Add( self.rbnJeeRootJavax, 0, wx.ALL, 5 )

        self.rbnJeeRootJakarta = wx.RadioButton( featuresSizer.GetStaticBox(), wx.ID_ANY, u"jakarta", wx.DefaultPosition, wx.DefaultSize, 0 )
        jeeRootPkgSizer.Add( self.rbnJeeRootJakarta, 0, wx.ALL, 5 )


        featureFormSizer.Add( jeeRootPkgSizer, 0, wx.EXPAND, 5 )


        featuresSizer.Add( featureFormSizer, 1, wx.EXPAND, 5 )


        mainSizer.Add( featuresSizer, 0, wx.ALL|wx.EXPAND, 5 )

        importSizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Imports" ), wx.VERTICAL )

        self.lscImport = wx.ListCtrl( importSizer.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_HRULES|wx.LC_REPORT|wx.LC_SINGLE_SEL )
        importSizer.Add( self.lscImport, 1, wx.ALL|wx.EXPAND, 5 )

        importFormSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
        importFormSizer.AddGrowableCol( 1 )
        importFormSizer.SetFlexibleDirection( wx.BOTH )
        importFormSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.lblModuleName = wx.StaticText( importSizer.GetStaticBox(), wx.ID_ANY, u"Package name:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.lblModuleName.Wrap( -1 )

        importFormSizer.Add( self.lblModuleName, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.txtModuleName = wx.TextCtrl( importSizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.txtModuleName.SetToolTip( u"Type in the name of a package that should be automatically imported in each generated code file" )

        importFormSizer.Add( self.txtModuleName, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )

        self.lblSymbolNames = wx.StaticText( importSizer.GetStaticBox(), wx.ID_ANY, u"Classes to import:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.lblSymbolNames.Wrap( -1 )

        importFormSizer.Add( self.lblSymbolNames, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.txtSymbolNames = wx.TextCtrl( importSizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_WORDWRAP )
        self.txtSymbolNames.SetToolTip( u"Type in the names of tclasses that should be imported from the above package in each generated code file.\nSeparate the names with spaces or commas" )
        self.txtSymbolNames.SetMinSize( wx.Size( -1,50 ) )

        importFormSizer.Add( self.txtSymbolNames, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )


        importSizer.Add( importFormSizer, 0, wx.EXPAND, 5 )

        buttonSizer = wx.BoxSizer( wx.HORIZONTAL )


        buttonSizer.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.btnAddImport = wx.Button( importSizer.GetStaticBox(), wx.ID_ANY, u"Add to list", wx.DefaultPosition, wx.DefaultSize, 0 )

        self.btnAddImport.SetBitmap( wx.Bitmap( self.asset_path( u"assets/icons/add.png" ), wx.BITMAP_TYPE_ANY ) )
        self.btnAddImport.SetToolTip( u"Add the above definition to the list of imports" )

        buttonSizer.Add( self.btnAddImport, 0, wx.ALL, 5 )

        self.btnUpdateImport = wx.Button( importSizer.GetStaticBox(), wx.ID_ANY, u"Update", wx.DefaultPosition, wx.DefaultSize, 0 )

        self.btnUpdateImport.SetBitmap( wx.Bitmap( self.asset_path( u"assets/icons/accept.png" ), wx.BITMAP_TYPE_ANY ) )
        self.btnUpdateImport.SetToolTip( u"Update the selected import" )

        buttonSizer.Add( self.btnUpdateImport, 0, wx.ALL, 5 )

        self.btnRemoveImport = wx.Button( importSizer.GetStaticBox(), wx.ID_ANY, u"Remove selected", wx.DefaultPosition, wx.DefaultSize, 0 )

        self.btnRemoveImport.SetBitmap( wx.Bitmap( self.asset_path( u"assets/icons/delete.png" ), wx.BITMAP_TYPE_ANY ) )
        self.btnRemoveImport.SetToolTip( u"Remove the selected import from the list" )

        buttonSizer.Add( self.btnRemoveImport, 0, wx.ALL, 5 )


        importSizer.Add( buttonSizer, 0, wx.EXPAND, 5 )


        mainSizer.Add( importSizer, 1, wx.ALL|wx.EXPAND, 5 )


        self.SetSizer( mainSizer )
        self.Layout()

        # Connect Events
        self.chkUseLombok.Bind( wx.EVT_CHECKBOX, self.chkUseLombokOnCheckBox )
        self.lscImport.Bind( wx.EVT_LIST_ITEM_SELECTED, self.lscImportOnListItemSelected )
        self.btnAddImport.Bind( wx.EVT_BUTTON, self.btnAddImportOnButtonClick )
        self.btnUpdateImport.Bind( wx.EVT_BUTTON, self.btnUpdateImportOnButtonClick )
        self.btnRemoveImport.Bind( wx.EVT_BUTTON, self.btnRemoveImportOnButtonClick )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def chkUseLombokOnCheckBox( self, event ):
        event.Skip()

    def lscImportOnListItemSelected( self, event ):
        event.Skip()

    def btnAddImportOnButtonClick( self, event ):
        event.Skip()

    def btnUpdateImportOnButtonClick( self, event ):
        event.Skip()

    def btnRemoveImportOnButtonClick( self, event ):
        event.Skip()

    # Virtual image path resolution method. Override this in your derived class.
    def asset_path( self, bitmap_path ):
        return bitmap_path


###########################################################################
## Class CSharpOptionPageBase
###########################################################################

class CSharpOptionPageBase ( wx.Panel ):

    def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,400 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
        wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

        mainSizer = wx.BoxSizer( wx.VERTICAL )

        featuresSizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Additional features" ), wx.HORIZONTAL )

        self.chkAddEFCoreAttrib = wx.CheckBox( featuresSizer.GetStaticBox(), wx.ID_ANY, u"Add EFCore data annotations", wx.DefaultPosition, wx.DefaultSize, 0 )
        featuresSizer.Add( self.chkAddEFCoreAttrib, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


        mainSizer.Add( featuresSizer, 0, wx.ALL|wx.EXPAND, 5 )

        importSizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Imports" ), wx.VERTICAL )

        self.lscImport = wx.ListCtrl( importSizer.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_HRULES|wx.LC_REPORT|wx.LC_SINGLE_SEL )
        importSizer.Add( self.lscImport, 1, wx.ALL|wx.EXPAND, 5 )

        formSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
        formSizer.AddGrowableCol( 1 )
        formSizer.SetFlexibleDirection( wx.BOTH )
        formSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.lblModuleName = wx.StaticText( importSizer.GetStaticBox(), wx.ID_ANY, u"Namespace:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.lblModuleName.Wrap( -1 )

        formSizer.Add( self.lblModuleName, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.txtModuleName = wx.TextCtrl( importSizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.txtModuleName.SetToolTip( u"Type in the name of a namespace that should be automatically imported in each generated code file" )

        formSizer.Add( self.txtModuleName, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )

        self.lblSymbolNames = wx.StaticText( importSizer.GetStaticBox(), wx.ID_ANY, u"Types to import:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.lblSymbolNames.Wrap( -1 )

        formSizer.Add( self.lblSymbolNames, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.txtSymbolNames = wx.TextCtrl( importSizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_WORDWRAP )
        self.txtSymbolNames.SetMinSize( wx.Size( -1,60 ) )

        formSizer.Add( self.txtSymbolNames, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )


        importSizer.Add( formSizer, 0, wx.EXPAND, 5 )

        buttonSizer = wx.BoxSizer( wx.HORIZONTAL )


        buttonSizer.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.btnAddImport = wx.Button( importSizer.GetStaticBox(), wx.ID_ANY, u"Add to list", wx.DefaultPosition, wx.DefaultSize, 0 )

        self.btnAddImport.SetBitmap( wx.Bitmap( self.asset_path( u"assets/icons/add.png" ), wx.BITMAP_TYPE_ANY ) )
        self.btnAddImport.SetToolTip( u"Add the above definition to the list of imports" )

        buttonSizer.Add( self.btnAddImport, 0, wx.ALL, 5 )

        self.btnUpdateImport = wx.Button( importSizer.GetStaticBox(), wx.ID_ANY, u"Update", wx.DefaultPosition, wx.DefaultSize, 0 )

        self.btnUpdateImport.SetBitmap( wx.Bitmap( self.asset_path( u"assets/icons/accept.png" ), wx.BITMAP_TYPE_ANY ) )
        self.btnUpdateImport.SetToolTip( u"Update the selected import" )

        buttonSizer.Add( self.btnUpdateImport, 0, wx.ALL, 5 )

        self.btnRemoveImport = wx.Button( importSizer.GetStaticBox(), wx.ID_ANY, u"Remove selected", wx.DefaultPosition, wx.DefaultSize, 0 )

        self.btnRemoveImport.SetBitmap( wx.Bitmap( self.asset_path( u"assets/icons/delete.png" ), wx.BITMAP_TYPE_ANY ) )
        self.btnRemoveImport.SetToolTip( u"Remove the selected import from the list" )

        buttonSizer.Add( self.btnRemoveImport, 0, wx.ALL, 5 )


        importSizer.Add( buttonSizer, 0, wx.EXPAND, 5 )


        mainSizer.Add( importSizer, 1, wx.ALL|wx.EXPAND, 5 )


        self.SetSizer( mainSizer )
        self.Layout()

        # Connect Events
        self.lscImport.Bind( wx.EVT_LIST_ITEM_SELECTED, self.lscImportOnListItemSelected )
        self.btnAddImport.Bind( wx.EVT_BUTTON, self.btnAddImportOnButtonClick )
        self.btnUpdateImport.Bind( wx.EVT_BUTTON, self.btnUpdateImportOnButtonClick )
        self.btnRemoveImport.Bind( wx.EVT_BUTTON, self.btnRemoveImportOnButtonClick )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def lscImportOnListItemSelected( self, event ):
        event.Skip()

    def btnAddImportOnButtonClick( self, event ):
        event.Skip()

    def btnUpdateImportOnButtonClick( self, event ):
        event.Skip()

    def btnRemoveImportOnButtonClick( self, event ):
        event.Skip()

    # Virtual image path resolution method. Override this in your derived class.
    def asset_path( self, bitmap_path ):
        return bitmap_path


###########################################################################
## Class SqlOptionPageBase
###########################################################################

class SqlOptionPageBase ( wx.Panel ):

    def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 600,400 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
        wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

        mainSizer = wx.BoxSizer( wx.VERTICAL )

        rbxDialectChoices = [ u"Generic", u"MySQL", u"PostgreSQL", u"Firebird", u"Oracle", u"DB2", u"SQL Server", u"Sybase", u"Access", u"SQLite", u"Derby", u"HSQLDB", u"H2" ]
        self.rbxDialect = wx.RadioBox( self, wx.ID_ANY, u"SQL Dialect", wx.DefaultPosition, wx.DefaultSize, rbxDialectChoices, 7, wx.RA_SPECIFY_COLS )
        self.rbxDialect.SetSelection( 0 )
        self.rbxDialect.SetToolTip( u"Select the SQL dialect that should be used in generated scripts" )

        mainSizer.Add( self.rbxDialect, 0, wx.ALL|wx.EXPAND, 5 )

        scriptSizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Script generation" ), wx.VERTICAL )

        numScriptSizer = wx.BoxSizer( wx.HORIZONTAL )

        self.rbnSingleScript = wx.RadioButton( scriptSizer.GetStaticBox(), wx.ID_ANY, u"Generate a single database script", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.rbnSingleScript.SetToolTip( u"Select to generate a single file with all the table and foreign keys definitions" )

        numScriptSizer.Add( self.rbnSingleScript, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.rbnMultiScript = wx.RadioButton( scriptSizer.GetStaticBox(), wx.ID_ANY, u"Generate a script per table", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.rbnMultiScript.SetToolTip( u"Select to generate a specific script for each table and a separate foreign keys script" )

        numScriptSizer.Add( self.rbnMultiScript, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


        scriptSizer.Add( numScriptSizer, 1, wx.EXPAND, 5 )

        scriptFormSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
        scriptFormSizer.AddGrowableCol( 1 )
        scriptFormSizer.SetFlexibleDirection( wx.BOTH )
        scriptFormSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        labelSizer = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText14 = wx.StaticText( scriptSizer.GetStaticBox(), wx.ID_ANY, u"Script filename", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText14.SetLabelMarkup( u"Script filename" )
        self.m_staticText14.Wrap( -1 )

        labelSizer.Add( self.m_staticText14, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )

        self.m_staticText15 = wx.StaticText( scriptSizer.GetStaticBox(), wx.ID_ANY, u"(without extension):", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText15.Wrap( -1 )

        labelSizer.Add( self.m_staticText15, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )


        scriptFormSizer.Add( labelSizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )

        self.txtScriptFilename = wx.TextCtrl( scriptSizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.txtScriptFilename.SetToolTip( u"Enter the name of the unique script file without the \".sql\" extension" )

        scriptFormSizer.Add( self.txtScriptFilename, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )


        scriptSizer.Add( scriptFormSizer, 1, wx.EXPAND, 5 )


        mainSizer.Add( scriptSizer, 0, wx.ALL|wx.EXPAND, 5 )


        self.SetSizer( mainSizer )
        self.Layout()

        # Connect Events
        self.rbnSingleScript.Bind( wx.EVT_RADIOBUTTON, self.onScriptRadioButtonClicked )
        self.rbnMultiScript.Bind( wx.EVT_RADIOBUTTON, self.onScriptRadioButtonClicked )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def onScriptRadioButtonClicked( self, event ):
        event.Skip()


    # Virtual image path resolution method. Override this in your derived class.
    def asset_path( self, bitmap_path ):
        return bitmap_path


