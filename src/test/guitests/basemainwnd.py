#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest

import wx

from core.application import Application
from gui.MainWindow import MainWindow
from gui.guiconfig import GeneralGuiConfig


class BaseMainWndTest(unittest.TestCase):
	def _processEvents (self):
		"""
		Обработать накопившиеся сообщения
		"""
		count = 0

		loop = wx.EventLoop.GetActive()
		app = wx.GetApp()
		
		while app.Pending():
			count += 1
			app.Dispatch()

		return count


	def setUp(self):
		generalConfig = GeneralGuiConfig (Application.config)
		generalConfig.askBeforeExitOption.value = False

		self.wnd = MainWindow (None, -1, "")
		Application.mainWindow = self.wnd
		wx.GetApp().SetTopWindow (self.wnd)
		#self._processEvents()


	def tearDown (self):
		self.wnd.Close()
		self.wnd.Hide()
		self._processEvents()
