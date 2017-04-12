# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.aui
import wx.grid

###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1 ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Instrument Controller", pos = wx.DefaultPosition, size = wx.Size( 721,409 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		self.m_mgr = wx.aui.AuiManager()
		self.m_mgr.SetManagedWindow( self )
		self.m_mgr.SetFlags(wx.aui.AUI_MGR_DEFAULT)
		
		self.m_auinotebook4 = wx.aui.AuiNotebook( self, wx.ID_ANY, wx.Point( 0,0 ), wx.Size( 500,700 ), 0 )
		self.m_mgr.AddPane( self.m_auinotebook4, wx.aui.AuiPaneInfo() .Left() .CloseButton( False ).MaximizeButton( True ).MinimizeButton( True ).PinButton( True ).Dock().Resizable().FloatingSize( wx.Size( 800,550 ) ) )
		
		self.m_panel5 = wx.Panel( self.m_auinotebook4, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
		gbSizer4 = wx.GridBagSizer( 0, 0 )
		gbSizer4.SetFlexibleDirection( wx.BOTH )
		gbSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_grid7 = wx.grid.Grid( self.m_panel5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
		# Grid
		self.m_grid7.CreateGrid( 5, 5 )
		self.m_grid7.EnableEditing( True )
		self.m_grid7.EnableGridLines( True )
		self.m_grid7.EnableDragGridSize( False )
		self.m_grid7.SetMargins( 0, 0 )
		
		# Columns
		self.m_grid7.EnableDragColMove( False )
		self.m_grid7.EnableDragColSize( True )
		self.m_grid7.SetColLabelSize( 30 )
		self.m_grid7.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Rows
		self.m_grid7.EnableDragRowSize( True )
		self.m_grid7.SetRowLabelSize( 80 )
		self.m_grid7.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		self.m_grid7.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		gbSizer4.Add( self.m_grid7, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		
		self.m_panel5.SetSizer( gbSizer4 )
		self.m_panel5.Layout()
		gbSizer4.Fit( self.m_panel5 )
		self.m_auinotebook4.AddPage( self.m_panel5, u"Control", True, wx.NullBitmap )
		
		self.m_auinotebook5 = wx.aui.AuiNotebook( self, wx.ID_ANY, wx.Point( 0,500 ), wx.Size( 500,700 ), 0 )
		self.m_mgr.AddPane( self.m_auinotebook5, wx.aui.AuiPaneInfo() .Center() .CloseButton( False ).MaximizeButton( True ).MinimizeButton( True ).PinButton( True ).Dock().Resizable().FloatingSize( wx.Size( 500,700 ) ) )
		
		self.m_scrolledWindow1 = wx.ScrolledWindow( self.m_auinotebook5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.m_scrolledWindow1.SetScrollRate( 5, 5 )
		gbSizer5 = wx.GridBagSizer( 0, 0 )
		gbSizer5.SetFlexibleDirection( wx.BOTH )
		gbSizer5.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.RunButton = wx.Button( self.m_scrolledWindow1, wx.ID_ANY, u"Run", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer5.Add( self.RunButton, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.ResetButton = wx.Button( self.m_scrolledWindow1, wx.ID_ANY, u"Reset", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer5.Add( self.ResetButton, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.SaveButton = wx.Button( self.m_scrolledWindow1, wx.ID_ANY, u"Save Data", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer5.Add( self.SaveButton, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.GraphButton = wx.Button( self.m_scrolledWindow1, wx.ID_ANY, u"Save Graph", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer5.Add( self.GraphButton, wx.GBPosition( 0, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText9 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Port", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )
		gbSizer5.Add( self.m_staticText9, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.PortBox = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer5.Add( self.PortBox, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.HarmonicsLable = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Harmonics", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.HarmonicsLable.Wrap( -1 )
		gbSizer5.Add( self.HarmonicsLable, wx.GBPosition( 1, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.HarmonicsBox = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer5.Add( self.HarmonicsBox, wx.GBPosition( 1, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText11 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Export Name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )
		gbSizer5.Add( self.m_staticText11, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.NameBox = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer5.Add( self.NameBox, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText12 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Number of bursts", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )
		gbSizer5.Add( self.m_staticText12, wx.GBPosition( 2, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.BurstsBox = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer5.Add( self.BurstsBox, wx.GBPosition( 2, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText13 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Number of readings", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText13.Wrap( -1 )
		gbSizer5.Add( self.m_staticText13, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.ReadingsBox = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer5.Add( self.ReadingsBox, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.m_staticText14 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Measure Time (s)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText14.Wrap( -1 )
		gbSizer5.Add( self.m_staticText14, wx.GBPosition( 3, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.TimeBox = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer5.Add( self.TimeBox, wx.GBPosition( 3, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.ForcedRangeLabel = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Forced Range", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.ForcedRangeLabel.Wrap( -1 )
		gbSizer5.Add( self.ForcedRangeLabel, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.RangeBox = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer5.Add( self.RangeBox, wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.ACDCcheck = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"ACDC RMS", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer5.Add( self.ACDCcheck, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.ACcheck = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"AC RMS", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer5.Add( self.ACcheck, wx.GBPosition( 5, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.MEANcheck = wx.CheckBox( self.m_scrolledWindow1, wx.ID_ANY, u"MEAN (|v|)", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer5.Add( self.MEANcheck, wx.GBPosition( 5, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		
		self.m_scrolledWindow1.SetSizer( gbSizer5 )
		self.m_scrolledWindow1.Layout()
		gbSizer5.Fit( self.m_scrolledWindow1 )
		self.m_auinotebook5.AddPage( self.m_scrolledWindow1, u"Graph", True, wx.NullBitmap )
		
		
		self.m_mgr.Update()
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.OnClose )
		self.RunButton.Bind( wx.EVT_BUTTON, self.OnRun )
		self.ResetButton.Bind( wx.EVT_BUTTON, self.OnReset )
		self.SaveButton.Bind( wx.EVT_BUTTON, self.OnSave )
		self.GraphButton.Bind( wx.EVT_BUTTON, self.OnGraph )
	
	def __del__( self ):
		self.m_mgr.UnInit()
		
	
	
	# Virtual event handlers, overide them in your derived class
	def OnClose( self, event ):
		event.Skip()
	
	def OnRun( self, event ):
		event.Skip()
	
	def OnReset( self, event ):
		event.Skip()
	
	def OnSave( self, event ):
		event.Skip()
	
	def OnGraph( self, event ):
		event.Skip()
	

