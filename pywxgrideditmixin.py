import wx
import wx.grid
"""
Mixin for wx.grid to implement cut/copy/paste and undo/redo.
Handlers are in the method Key below.  Other handlers (e.g., menu, toolbar) should call the functions in OnMixinKeypress.
https://github.com/wleepang/MMFitter/blob/master/pywxgrideditmixin.py
"""
class PyWXGridEditMixin():
    """ A Copy/Paste and undo/redo mixin for wx.grid. Undo/redo is per-table, not yet global."""
    def __init_mixin__(self):
        """caller must invoke this method to enable keystrokes, or call these handlers if they are overridden."""
        wx.EVT_KEY_DOWN(self, self.OnMixinKeypress)
        wx.grid.EVT_GRID_CELL_CHANGE(self, self.Mixin_OnCellChange)
        wx.grid.EVT_GRID_EDITOR_SHOWN(self, self.Mixin_OnCellEditor)
        self._undoStack = []
        self._redoStack = []
        self._stackPtr = 0

    def OnMixinKeypress(self, event):
        """Keystroke handler."""
        key = event.GetKeyCode() 
        if key == ord(" ") and event.ShiftDown and not event.ControlDown:
            self.SelectRow(self.GetGridCursorRow())
            return

        if not event.ControlDown: return
        if key == 67: self.Copy()
        elif key == 86: self.OnPaste()
        elif key == ord("X"): self.OnCut()
        elif key == wx.WXK_DELETE: self.Delete()
        elif key == ord("Z"): self.Undo()
        elif key == ord("Y"): self.Redo()
        elif key == ord(" "): self.SelectCol(self.GetGridCursorCol())
        elif key: event.Skip()

    def Mixin_OnCellEditor(self, evt=None):
        """this method saves the value of cell before it's edited (when that value disappears)"""
        top, left, rows, cols = self.GetSelectionBox()[0]
        v = self.GetCellValue(top, left)
        self._editOldValue = v+"\n"

    def Mixin_OnCellChange(self, evt):
        """Undo/redo handler Use saved value from above for undo."""
        box = self.GetSelectionBox()[0]
        newValue = self.GetCellValue(*box[:2])
        self.AddUndo(undo=(self.Paste, (box, self._editOldValue)),
            redo=(self.Paste, (box, newValue)))
        self._editOldValue = None
    
    def GetSelectionBox(self):
        """Produce a set of selection boxes of the form (top, left, nrows, ncols)"""
        #For wxGrid, blocks, cells, rows and cols all have different selection notations.  
        #This captures them all into a single "box" tuple (top, left, rows, cols)
        gridRows = self.GetNumberRows()
        gridCols = self.GetNumberCols()
        tl, br = self.GetSelectionBlockTopLeft(), self.GetSelectionBlockBottomRight()
        # need to reorder based on what should get copy/pasted first
        boxes = []
        # collect top, left, rows, cols in boxes for each selection
        for blk in range(len(tl)):
            boxes.append((tl[blk][0], tl[blk][1], br[blk][0] - tl[blk][0]+1, br[blk][1]-tl[blk][1]+1))
        for row in self.GetSelectedRows():
            boxes.append((row, 0, 1, gridCols))
        for col in self.GetSelectedCols():
            boxes.append((0, col, gridRows, 1))
        # if not selecting rows, cols, or blocks, add the current cursor (this is not picked up in GetSelectedCells
        if len(boxes) ==0:
            boxes.append((self.GetGridCursorRow(), self.GetGridCursorCol(), 1, 1))
        for (top, left) in self.GetSelectedCells():
                boxes.append((top, left, 1, 1)) # single cells are 1x1 rowsxcols.
        return boxes

    def Copy(self):
        """Copy selected range into clipboard.  If more than one range is selected at a time, only the first is copied"""
        top, left, rows,cols = self.GetSelectionBox()[0]
        
        data = self.Box2String(top, left, rows, cols, True, True)
        # Create text data object for use by TheClipboard
        clipboard = wx.TextDataObject()
        clipboard.SetText(data)
        # Put the data in the clipboard
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(clipboard)
            wx.TheClipboard.Close()
        else:
            print "Can't open the clipboard"

    def Box2String(self, top, left, rows, cols, getRowLabels=False, getColLabels=False):
        """Return values in a selected cell range as a string.  This is used to pass text to clipboard."""
        data = '' # collect strings in grid for clipboard
        # Tabs '\t' separate cols and '\n' separate rows
        
        # retrieve the row and column labels
        # WLP: added options to retrieve row and column labels
        
        if getColLabels:
            colLabels = [self.GetColLabelValue(c) for c in range(left, left+cols)]
            colLabels = str.join('\t', colLabels) + '\n'
            if getRowLabels:
                colLabels = '\t' + colLabels
            
            data += colLabels
        
        for r in range(top, top+rows):
            rowAsString = [str(self.GetCellValue(r, c)) for c in range(left, left+cols) if self.CellInGrid(r,c)]
            rowAsString = str.join('\t', rowAsString) + '\n'
            if getRowLabels:
                rowAsString = self.GetRowLabelValue(r) + '\t' + rowAsString
            
            data += rowAsString
        return data    

    def OnPaste(self):
        """Event handler to paste from clipboard into grid.  Data assumed to be separated by tab (columns) and "\n" (rows)."""
        clipboard = wx.TextDataObject()
        if wx.TheClipboard.Open():
            wx.TheClipboard.GetData(clipboard)
            wx.TheClipboard.Close()
        else:
            print "Can't open the clipboard"
        data = clipboard.GetText()
        table = [r.split('\t') for r in data.splitlines()] # convert to array

        #Determine the paste area given the size of the data in the clipboard (clipBox) and the current selection (selBox)
        top, left, selRows,selCols = self.GetSelectionBox()[0]
        if len(table) ==0 or type(table[0]) is not list: table = [table]
        pBox = self._DeterminePasteArea(top, left, len(table), len(table[0]), selRows, selCols)
        self.AddUndo(undo=(self.Paste, (pBox, self.Box2String(*pBox))),
            redo=(self.Paste, (pBox, data)))
        self.Paste(pBox, data)

    def _DeterminePasteArea(self, top, left, clipRows, clipCols, selRows, selCols):
        """paste area rules: if 1-d selection (either directon separately) and 2-d clipboard, use clipboard size, otherwise use selection size"""
        pRows = selRows ==1 and clipRows > 1 and clipRows or selRows
        pCols = selCols ==1 and clipCols > 1 and clipCols or selCols
        return top, left, pRows, pCols
        
        if clipRows ==1 and clipCols ==1: # constrain paste range by what's in clipboard
            pRows, pCols = clipRows, clipCols 
        else: # constrain paste range by current selection
            pRows, pCols = selRows, selCols
        return top, left, pRows, pCols # the actual area we'll paste into
        
    def Paste(self, box, dataString):
        top, left, rows, cols = box
        data = [r.split('\t') for r in dataString.splitlines()]
        if len(data) ==0 or type(data[0]) is not list: data = [data]
        # get sizes (rows, cols) of both clipboard and current selection
        dataRows, dataCols = len(data), len(data[0])
        for r in range(rows):
            row = top + r
            for c in range(cols):
                col = left + c
                if self.CellInGrid(row, col): self.SetCellValue(row, col, data[r %dataRows][c % dataCols])
        return

    def CellInGrid(self, r, c): # only paste data that actually falls on the table
        return r >=0 and c >=0 and r < self.GetNumberRows() and c < self.GetNumberCols()

    def OnCut(self):
        """Cut cells from grid into clipboard"""
        box = self.GetSelectionBox()[0]
        self.Copy()
        self.Delete() #this takes care of undo/redo

    def Delete(self):
        """Clear Cell contents"""
        boxes = self.GetSelectionBox()
        for box in boxes: #allow multiple selection areas to be deleted
            # first, save data in undo stack
            self.AddUndo(undo=(self.Paste, (box, self.Box2String(*box))),
                redo=(self.Paste, (box, "\n")))
            self.Paste(box, "\n")

    def AddUndo(self, undo, redo):
        """Add an undo/redo combination to the respective stack"""
        (meth, parms) = undo
        #print self._stackPtr, "set undo: ",parms, "redo=",redo[1]
        self._undoStack.append((meth, parms))
        (meth, parms) = redo
        self._redoStack.append((meth, parms))
        self._stackPtr+= 1
        # remove past undos beyond the current one.
        self._undoStack = self._undoStack[:self._stackPtr]
        self._redoStack = self._redoStack[:self._stackPtr]

    def Undo(self, evt = None):
        if self._stackPtr > 0:
            self._stackPtr -= 1
            (funct, params) = self._undoStack[self._stackPtr]
            #print "UNdoing:"+`self._stackPtr`+"=",`params[0]`
            funct(*params)
            # set cursor at loc asd selection if block
            top, left, rows, cols = params[0]
            self.SelectBlock(top, left, top+rows-1, left+cols-1)
            self.SetGridCursor(top,left)

    def Redo(self, evt = None):
        if self._stackPtr < len(self._redoStack):
            (funct, params) = self._redoStack[self._stackPtr]
            #print "REdoing:"+`self._stackPtr`+"=",`params[0]`
            funct(*params)
            # set cursor at loc
            top, left, rows, cols = params[0]
            self.SetGridCursor(top, left)
            self.SelectBlock(top, left, top+rows-1, left+cols-1)
            self._stackPtr += 1

if __name__ == '__main__':
        import sys
        app = wx.PySimpleApp()
        frame = wx.Frame(None, -1, size=(700,500), title = "wx.Grid example")

        grid = wx.grid.Grid(frame)
        grid.CreateGrid(20,6)

        # To add capability, mix it in, then set key handler, or add call to grid.Key() in your own handler
        wx.grid.Grid.__bases__ += (PyWXGridEditMixin,)
        grid.__init_mixin__()

        grid.SetDefaultColSize(70, 1)
        grid.EnableDragGridSize(False)
        
        grid.SetCellValue(0,0,"Col is")
        grid.SetCellValue(1,0,"Read Only")
        grid.SetCellValue(1,1,"hello")
        grid.SetCellValue(2,1,"23")
        grid.SetCellValue(4,3,"greren")
        grid.SetCellValue(5,3,"geeges")
        
        # make column 1 multiline, autowrap
        cattr = wx.grid.GridCellAttr()
        cattr.SetEditor(wx.grid.GridCellAutoWrapStringEditor())
        #cattr.SetRenderer(wx.grid.GridCellAutoWrapStringRenderer())
        grid.SetColAttr(1, cattr)
        
        frame.Show(True)
        app.MainLoop()