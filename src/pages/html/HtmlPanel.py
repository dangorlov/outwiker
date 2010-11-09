# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Sun Apr 18 22:17:12 2010

import os
#import md5
from abc import ABCMeta, abstractmethod

import wx

from core.controller import Controller
from gui.BaseTextPanel import BaseTextPanel
import core.system
from gui.htmlview import HtmlView
from gui.TextEditor import TextEditor
import core.commands

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode

# end wxGlade


class ToolsInfo (object):
	def __init__ (self, id, alwaysEnabled):
		"""
		id - идентификатор
		alwaysEnabled - кнопка всегда активна?
		"""
		self.id = id
		self.alwaysEnabled = alwaysEnabled


class HtmlPanel(BaseTextPanel):
	__metaclass__ = ABCMeta
	
	def __init__(self, *args, **kwds):
		BaseTextPanel.__init__ (self, *args, **kwds)
		self._htmlFile = "__content.html"
		self.currentHtmlFile = None

		self.imagesDir = core.system.getImagesDir()

		# begin wxGlade: HtmlPanel.__init__
		kwds["style"] = wx.TAB_TRAVERSAL
		wx.Panel.__init__(self, *args, **kwds)
		self.HtmlView = wx.Notebook(self, -1, style=wx.NB_BOTTOM)
		self.previewPane = wx.Panel(self.HtmlView, -1)
		self.htmlPane = wx.Panel(self.HtmlView, -1)
		self.codeWindow = TextEditor (self.htmlPane, -1)
		self.htmlWindow = HtmlView(self.previewPane, -1)

		self.__set_properties()
		self.__do_layout()

		self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.onTabChanged, self.HtmlView)
		# end wxGlade

		self.HCount = 6
		self.toolsId = {}

	
	def onEditorConfigChange (self):
		self.codeWindow.setDefaultSettings()

	
	def onClose (self, event):
		BaseTextPanel.Close (self)


	def onAttachmentPaste (self, fnames):
		text = self._getAttachString (fnames)
		self.codeWindow.textCtrl.AddText (text)
		self.codeWindow.textCtrl.SetFocus()

	
	def UpdateView (self, page):
		self.htmlWindow.page = self._currentpage
		self.codeWindow.textCtrl.SetText (self._currentpage.content)
		self.codeWindow.textCtrl.EmptyUndoBuffer()
		self.codeWindow.textCtrl.SetReadOnly (page.readonly)


	def GetContentFromGui(self):
		return self.codeWindow.textCtrl.GetText()
	
	
	def __set_properties(self):
		# begin wxGlade: HtmlPanel.__set_properties
		pass
		# end wxGlade


	def __do_layout(self):
		# begin wxGlade: HtmlPanel.__do_layout
		grid_sizer_7 = wx.FlexGridSizer(1, 1, 0, 0)
		grid_sizer_9 = wx.FlexGridSizer(1, 1, 0, 0)
		grid_sizer_8 = wx.FlexGridSizer(1, 1, 0, 0)
		grid_sizer_8.Add(self.codeWindow, 1, wx.TOP|wx.BOTTOM|wx.EXPAND, 2)
		self.htmlPane.SetSizer(grid_sizer_8)
		grid_sizer_8.AddGrowableRow(0)
		grid_sizer_8.AddGrowableCol(0)
		grid_sizer_9.Add(self.htmlWindow, 1, wx.EXPAND, 0)
		self.previewPane.SetSizer(grid_sizer_9)
		grid_sizer_9.AddGrowableRow(0)
		grid_sizer_9.AddGrowableCol(0)
		self.HtmlView.AddPage(self.htmlPane, "HTML")
		self.HtmlView.AddPage(self.previewPane, "Preview")
		grid_sizer_7.Add(self.HtmlView, 1, wx.EXPAND, 0)
		self.SetSizer(grid_sizer_7)
		grid_sizer_7.Fit(self)
		grid_sizer_7.AddGrowableRow(0)
		grid_sizer_7.AddGrowableCol(0)
		# end wxGlade

		self.Bind (wx.EVT_CLOSE, self.onClose)


	@abstractmethod
	def generateHtml (self, page, path):
		pass


	def getHtmlPath (self, path):
		"""
		Получить путь до результирующего файла HTML
		"""
		path = os.path.join (self._currentpage.path, self._htmlFile)
		return path


	def removeHtml (self):
		"""
		Удалить сгенерированный HTML-файл
		"""
		if self.currentHtmlFile != None:
			try:
				os.remove (self.currentHtmlFile)
			except OSError:
				pass


	def onTabChanged(self, event): # wxGlade: HtmlPanel.<event_handler>
		if self._currentpage == None:
			return

		if event.GetSelection() == 1:
			self.Save()
			self._enableTools (self.pageToolsMenu, False)
			self.htmlWindow.SetFocus()
			self.htmlWindow.Update()
			self.__showHtml()
		else:
			#self.removeHtml()
			self.codeWindow.SetFocus()
			self._enableTools (self.pageToolsMenu, True)
	

	def __showHtml (self):
		"""
		Подготовить и показать HTML текущей страницы
		"""
		assert self._currentpage != None

		core.commands.setStatusText (_(u"Page rendered. Please wait...") )
		Controller.instance().onHtmlRenderingBegin (self._currentpage, self.htmlWindow)

		path = self.getHtmlPath (self._currentpage)
		self.currentHtmlFile = path
		try:
			self.generateHtml (self._currentpage, path)
			self.htmlWindow.LoadPage (path)
		except IOError:
			wx.MessageBox (_(u"Can't save HTML-file"), _(u"Error"), wx.ICON_ERROR | wx.OK)

		core.commands.setStatusText (u"")
		Controller.instance().onHtmlRenderingEnd (self._currentpage, self.htmlWindow)
	

	def _enableTools (self, menu, enable):
		for key in self.toolsId:
			if not self.toolsId[key].alwaysEnabled:
				self.mainWindow.mainToolbar.EnableTool (self.toolsId[key].id, enable)
				menu.Enable (self.toolsId[key].id, enable)
	

	def GetSearchPanel (self):
		return self.codeWindow.searchPanel


	def _removeTool (self, id):
		self.mainWindow.mainToolbar.DeleteTool (id)
		self.mainWindow.Unbind(wx.EVT_MENU, id=id)


	def _addRenderTools (self):
		self._addTool (self.pageToolsMenu, 
				"ID_RENDER", 
				self.__switchView, 
				_(u"Code / Preview\tF5"), 
				_(u"Code / Preview"), 
				os.path.join (self.imagesDir, "render.png"),
				True)


	def __switchView (self, event):
		if self._currentpage == None:
			return

		if self.HtmlView.GetSelection() == 0:
			self.HtmlView.SetSelection (1)
		else:
			self.HtmlView.SetSelection (0)


	def _addTool (self, menu, idstring, func, menuText, buttonText, image, alwaysEnabled = False):
		"""
		Добавить пункт меню и кнопку на панель
		menu -- меню для добавления элемента
		id -- идентификатор меню и кнопки
		func -- обработчик
		menuText -- название пунта меню
		buttonText -- подсказка для кнопки
		image -- имя файла с картинкой
		disableOnView -- дизаблить кнопку при переключении на просмотр результата
		"""
		id = wx.NewId()
		self.toolsId[idstring] = ToolsInfo (id, alwaysEnabled)

		menu.Append (id, menuText, "", wx.ITEM_NORMAL)
		self.mainWindow.Bind(wx.EVT_MENU, func, id = id)

		self.mainWindow.mainToolbar.AddLabelTool(id, 
				buttonText, 
				wx.Bitmap(image, wx.BITMAP_TYPE_ANY), 
				wx.NullBitmap, 
				wx.ITEM_NORMAL, 
				buttonText, 
				"")
	

	def removeGui (self):
		BaseTextPanel.removeGui (self)

		for key in self.toolsId.keys ():
			self._removeTool (self.toolsId[key].id)


	def _turnText (self, lefttext, righttext):
		selText = self.codeWindow.textCtrl.GetSelectedText()
		newtext = lefttext + selText + righttext
		self.codeWindow.textCtrl.ReplaceSelection (newtext)

		if len (selText) == 0:
			"""
			Если не оборачиваем текст, а делаем пустой тег, то поместим каретку до закрывающегося тега
			"""
			currPos = self.codeWindow.textCtrl.GetSelectionEnd()
			len_bytes = self.codeWindow.calcByteLen (righttext)

			newPos = currPos - len_bytes

			self.codeWindow.textCtrl.SetSelection (newPos, newPos)
	

	def _turnList (self, start, end, itemStart, itemEnd):
		"""
		Создать список
		"""
		selText = self.codeWindow.textCtrl.GetSelectedText()
		items = filter (lambda item: len (item.strip()) > 0, selText.split ("\n") )

		# Собираем все элементы
		if len (items) > 0:
			itemsList = reduce (lambda result, item: result + itemStart + item.strip() + itemEnd + "\n", items, u"")
		else:
			itemsList = itemStart + itemEnd + "\n"

		result = start + itemsList + end

		if len (end) == 0:
			# Если нет завершающего тега (как в викинотации), 
			# то не нужен перевод строки у последнего элемента
			result = result[: -1]

		self.codeWindow.textCtrl.ReplaceSelection (result)

		if len (items) == 0:
			endText = u"%s\n%s" % (itemEnd, end)
			len_bytes = self.codeWindow.calcByteLen (endText)

			currPos = self.codeWindow.textCtrl.GetSelectionEnd()
			newPos = currPos - len_bytes
			self.codeWindow.textCtrl.SetSelection (newPos, newPos)


	def _replaceText (self, text):
		self.codeWindow.textCtrl.ReplaceSelection (text)


# end of class HtmlPanel

class HtmlPagePanel (HtmlPanel):
	def __init__ (self, *args, **kwds):
		HtmlPanel.__init__ (self, *args, **kwds)

		self._htmlStylesSection = "HtmlStyles"
		self.setupHtmlStyles()
	

	def setupHtmlStyles (self):
		# Значения по умолчанию для стилей
		stylesdefault = {
				wx.stc.STC_H_TAG: "fore:#000080,bold",
				wx.stc.STC_H_TAGUNKNOWN: "fore:#FF0000",
				wx.stc.STC_H_ATTRIBUTE: "fore:#008080",
				wx.stc.STC_H_ATTRIBUTEUNKNOWN: "fore:#FF0000",
				wx.stc.STC_H_NUMBER: "fore:#000000",
				wx.stc.STC_H_DOUBLESTRING: "fore:#0000FF",
				wx.stc.STC_H_SINGLESTRING: "fore:#0000FF",
				wx.stc.STC_H_COMMENT: "fore:#12B535"
				}

		# Устанавливаемые стили
		styles = {}
		
		try:
			styles = self.loadStyles()
		except:
			styles = stylesdefault
			self.saveStyles(styles)
		
		self.codeWindow.textCtrl.SetLexer (wx.stc.STC_LEX_HTML)
		self.codeWindow.textCtrl.StyleClearAll()

		for key in styles.keys():
			self.codeWindow.textCtrl.StyleSetSpec (key, styles[key])

		tags = u"a abbr acronym address applet area b base basefont \
			bdo big blockquote body br button caption center \
			cite code col colgroup dd del dfn dir div dl dt em \
			fieldset font form frame frameset h1 h2 h3 h4 h5 h6 \
			head hr html i iframe img input ins isindex kbd label \
			legend li link map menu meta noframes noscript \
			object ol optgroup option p param pre q s samp \
			script select small span strike strong style sub sup \
			table tbody td textarea tfoot th thead title tr tt u ul \
			var xml xmlns"


		attributes = u"abbr accept-charset accept accesskey action align alink \
			alt archive axis background bgcolor border \
			cellpadding cellspacing char charoff charset checked cite \
			class classid clear codebase codetype color cols colspan \
			compact content coords \
			data datafld dataformatas datapagesize datasrc datetime \
			declare defer dir disabled enctype event \
			face for frame frameborder \
			headers height href hreflang hspace http-equiv \
			id ismap label lang language leftmargin link longdesc \
			marginwidth marginheight maxlength media method multiple \
			name nohref noresize noshade nowrap \
			object onblur onchange onclick ondblclick onfocus \
			onkeydown onkeypress onkeyup onload onmousedown \
			onmousemove onmouseover onmouseout onmouseup \
			onreset onselect onsubmit onunload \
			profile prompt readonly rel rev rows rowspan rules \
			scheme scope selected shape size span src standby start style \
			summary tabindex target text title topmargin type usemap \
			valign value valuetype version vlink vspace width \
			text password checkbox radio submit reset \
			file hidden image"

		self.codeWindow.textCtrl.SetKeyWords (0, tags + attributes)
	

	def loadStyles (self):
		"""
		Загрузить стили из конфига
		"""
		config = wx.GetApp().getConfig()

		styles = {}

		styles[wx.stc.STC_H_TAG] = config.get (self._htmlStylesSection, "tag")
		styles[wx.stc.STC_H_TAGUNKNOWN] = config.get (self._htmlStylesSection, "tag_unknoun")
		styles[wx.stc.STC_H_ATTRIBUTE] = config.get (self._htmlStylesSection, "attribute")
		styles[wx.stc.STC_H_ATTRIBUTEUNKNOWN] = config.get (self._htmlStylesSection, "attribute_unknown")
		styles[wx.stc.STC_H_NUMBER] = config.get (self._htmlStylesSection, "number")
		styles[wx.stc.STC_H_DOUBLESTRING] = config.get (self._htmlStylesSection, "doublestring")
		styles[wx.stc.STC_H_SINGLESTRING] = config.get (self._htmlStylesSection, "singlestring")
		styles[wx.stc.STC_H_COMMENT] = config.get (self._htmlStylesSection, "comment")

		return styles

	
	def saveStyles (self, styles):
		config = wx.GetApp().getConfig()

		config.set (self._htmlStylesSection, "tag", styles[wx.stc.STC_H_TAG])
		config.set (self._htmlStylesSection, "tag_unknoun", styles[wx.stc.STC_H_TAGUNKNOWN])
		config.set (self._htmlStylesSection, "attribute", styles[wx.stc.STC_H_ATTRIBUTE])
		config.set (self._htmlStylesSection, "attribute_unknown", styles[wx.stc.STC_H_ATTRIBUTEUNKNOWN])
		config.set (self._htmlStylesSection, "number", styles[wx.stc.STC_H_NUMBER])
		config.set (self._htmlStylesSection, "doublestring", styles[wx.stc.STC_H_DOUBLESTRING])
		config.set (self._htmlStylesSection, "singlestring", styles[wx.stc.STC_H_SINGLESTRING])
		config.set (self._htmlStylesSection, "comment", styles[wx.stc.STC_H_COMMENT])


	def __addFontTools (self):
		"""
		Добавить инструменты, связанные со шрифтами
		"""
		self._addTool (self.pageToolsMenu, 
				"ID_BOLD", 
				lambda event: self._turnText (u"<b>", u"</b>"), 
				_(u"Bold\tCtrl+B"), 
				_(u"Bold (<b>...</b>)"), 
				os.path.join (self.imagesDir, "text_bold.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_ITALIC", 
				lambda event: self._turnText (u"<i>", u"</i>"), 
				_(u"Italic\tCtrl+I"), 
				_(u"Italic (<i>...</i>)"), 
				os.path.join (self.imagesDir, "text_italic.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_UNDERLINE", 
				lambda event: self._turnText (u"<u>", u"</u>"), 
				_(u"Underline\tCtrl+U"), 
				_(u"Underline (<u>...</u>)"), 
				os.path.join (self.imagesDir, "text_underline.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_SUBSCRIPT", 
				lambda event: self._turnText (u"<SUB>", u"</SUB>"), 
				_(u"Subscript\tCtrl+="), 
				_(u"Subscript (<sub> ... </sub>)"), 
				os.path.join (self.imagesDir, "text_subscript.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_SUPERSCRIPT", 
				lambda event: self._turnText (u"<SUP>", u"</SUP>"), 
				_(u"Superscript\tCtrl++"), 
				_(u"Superscript (<sup> ... </sup>)"), 
				os.path.join (self.imagesDir, "text_superscript.png"))

	
	def __addAlignTools (self):
		self._addTool (self.pageToolsMenu, 
				"ID_ALIGN_CENTER", 
				lambda event: self._turnText (u'<DIV ALIGN="CENTER">', u'</DIV>'), 
				_(u"Center align\tCtrl+Shift+C"), 
				_(u"Center align"), 
				os.path.join (self.imagesDir, "text_align_center.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_ALIGN_RIGHT", 
				lambda event: self._turnText (u'<DIV ALIGN="RIGHT">', u'</DIV>'), 
				_(u"Right align"), 
				_(u"Right align"), 
				os.path.join (self.imagesDir, "text_align_right.png"))
	

	def __addTableTools (self):
		"""
		Добавить инструменты, связанные с таблицами
		"""
		self._addTool (self.pageToolsMenu, 
				"ID_TABLE", 
				lambda event: self._turnText (u'<table>', u'</table>'), 
				_(u"Table\tCtrl+Q"), 
				_(u"Table (<table>...</table>)"), 
				os.path.join (self.imagesDir, "table.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_TABLE_TR", 
				lambda event: self._turnText (u'<tr>',u'</tr>'), 
				_(u"Table row\tCtrl+W"), 
				_(u"Table row (<tr>...</tr>)"), 
				os.path.join (self.imagesDir, "table_insert_row.png"))


		self._addTool (self.pageToolsMenu, 
				"ID_TABLE_TD", 
				lambda event: self._turnText (u'<td>', u'</td>'), 
				_(u"Table cell\tCtrl+Y"), 
				_(u"Table cell (<td>...</td>)"), 
				os.path.join (self.imagesDir, "table_insert_cell.png"))

	
	def __addListTools (self):
		"""
		Добавить инструменты, связанные со списками
		"""
		self._addTool (self.pageToolsMenu, 
				"ID_MARK_LIST", 
				lambda event: self._turnList (u'<ul>\n', u'</ul>', u'<li>', u'</li>'), 
				_(u"Bullets list\tCtrl+G"), 
				_(u"Bullets list (<ul>...</ul>)"), 
				os.path.join (self.imagesDir, "text_list_bullets.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_NUMBER_LIST", 
				lambda event: self._turnList (u'<ol>\n', u'</ol>', u'<li>', u'</li>'), 
				_(u"Numbers list\tCtrl+J"), 
				_(u"Numbers list (<ul>...</ul>)"), 
				os.path.join (self.imagesDir, "text_list_numbers.png"))
	

	def __addHTools (self):
		"""
		Добавить инструменты для заголовочных тегов <H>
		"""
		self._addTool (self.pageToolsMenu, 
				"ID_H1", 
				lambda event: self._turnText (u"<h1>", u"</h1>"), 
				_(u"H1\tCtrl+1"), 
				_(u"H1 (<h1>...</h1>)"), 
				os.path.join (self.imagesDir, "text_heading_1.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_H2", 
				lambda event: self._turnText (u"<h2>", u"</h2>"), 
				_(u"H2\tCtrl+2"), 
				_(u"H2 (<h2>...</h2>)"), 
				os.path.join (self.imagesDir, "text_heading_2.png"))
		
		self._addTool (self.pageToolsMenu, 
				"ID_H3", 
				lambda event: self._turnText (u"<h3>", u"</h3>"), 
				_(u"H3\tCtrl+3"), 
				_(u"H3 (<h3>...</h3>)"), 
				os.path.join (self.imagesDir, "text_heading_3.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_H4", 
				lambda event: self._turnText (u"<h4>", u"</h4>"), 
				_(u"H4\tCtrl+4"), 
				_(u"H4 (<h4>...</h4>)"), 
				os.path.join (self.imagesDir, "text_heading_4.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_H5", 
				lambda event: self._turnText (u"<h5>", u"</h5>"), 
				_(u"H5\tCtrl+5"), 
				_(u"H5 (<h5>...</h5>)"), 
				os.path.join (self.imagesDir, "text_heading_5.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_H6", 
				lambda event: self._turnText (u"<h6>", u"</h6>"), 
				_(u"H6\tCtrl+6"), 
				_(u"H6 (<h6>...</h6>)"), 
				os.path.join (self.imagesDir, "text_heading_6.png"))
	

	def __addOtherTools (self):
		"""
		Добавить остальные инструменты
		"""
		self._addTool (self.pageToolsMenu, 
				"ID_IMAGE", 
				lambda event: self._turnText (u'<img src="', u'"/>'), 
				u'Image\tCtrl+M', 
				u'Image (<img src="..."/>', 
				os.path.join (self.imagesDir, "image.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_LINK", 
				lambda event: self._turnText (u'<a href="">', u'</a>'), 
				_(u"Link\tCtrl+L"), 
				u'Link (<a href="...">...</a>)', 
				os.path.join (self.imagesDir, "link.png"))

		self._addTool (self.pageToolsMenu, 
				"ID_HORLINE", 
				lambda event: self._replaceText (u'<hr>'), 
				_(u"Horisontal line\tCtrl+H"), 
				_(u"Horisontal line (<hr>)"), 
				os.path.join (self.imagesDir, "text_horizontalrule.png"))


	def initGui (self, mainWindow):
		BaseTextPanel.initGui (self, mainWindow)

		self.pageToolsMenu = wx.Menu()
		
		self._addRenderTools()
		self.__addFontTools()
		self.__addAlignTools()
		self.__addHTools()
		self.__addTableTools()
		self.__addListTools()
		self.__addOtherTools()

		mainWindow.mainMenu.Insert (mainWindow.mainMenu.GetMenuCount() - 1, self.pageToolsMenu, "H&tml")
		mainWindow.mainToolbar.Realize()
		self.HtmlView.SetSelection (1)

	
	def generateHtml (self, page, path):
		if page.readonly and os.path.exists (path):
			# Если страница открыта только для чтения и html-файл уже существует, то покажем его
			return path

		template = u"<html><head><meta http-equiv='Content-Type' content='text/html; charset=UTF-8'/></head><body>%s</body></html>"

		text = page.content
		text = text.replace ("\r\n\r\n", "\n\n<p>")
		text = text.replace ("\n\n", "\n\n<p>")
		text = text.replace ("\n", "\n<br>")
		text = text.replace ("<br><li>", "\n<li>")

		text = template % text

		with open (path, "wb") as fp:
			fp.write (text.encode ("utf-8"))

		return path


	def removeGui (self):
		HtmlPanel.removeGui (self)
		self.mainWindow.mainMenu.Remove (self.mainWindow.mainMenu.GetMenuCount() - 2)
