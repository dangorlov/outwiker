#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from .tagscloud import TagsCloud, EVT_TAG_CLICK


class TagsPopup (wx.PopupTransientWindow):
    def __init__ (self, parent):
        wx.PopupTransientWindow.__init__ (self, parent)
        self.__tagsCloud = TagsCloud (self)
        self.__tagsCloud.Bind (EVT_TAG_CLICK, self.__onTagClick)

        sizer = wx.FlexGridSizer (1, 1)
        sizer.Add (self.__tagsCloud, 1, wx.EXPAND)
        sizer.AddGrowableRow (0)
        sizer.AddGrowableCol (0)

        self.SetSizer (sizer)
        self.Layout()


    def __onTagClick (self, event):
        wx.PostEvent(self, event)


    def setTags (self, taglist):
        self.__tagsCloud.setTags (taglist)


    def Popup (self):
        self.Layout()
        wx.PopupTransientWindow.Popup (self, self.__tagsCloud)
