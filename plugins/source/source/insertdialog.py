#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from .i18n import get_


class InsertDialog (wx.Dialog):
    """
    Диалог для вставки команды (:source:)
    """
    def __init__ (self, parent):
        global _
        _ = get_()

        super (InsertDialog, self).__init__ (parent, 
                style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.THICK_FRAME,
                title=_(u"Source code"))

        # Размер отступа
        self._indent = 50
        self._fieldsWidth = 200

        self.__createGui()
        self.fileCheckBox.SetFocus()
        self.Center(wx.CENTRE_ON_SCREEN)


    @property
    def language (self):
        return self.languageComboBox.GetValue()


    @property
    def tabWidth (self):
        return self.tabWidthSpin.GetValue()


    @property
    def languageIndex (self):
        return self.languageComboBox.GetCurrentSelection()


    @property
    def attachment (self):
        return self.attachmentComboBox.GetValue()


    @property
    def encoding (self):
        return self.encodingComboBox.GetValue()


    @property
    def insertFromFile (self):
        return self.fileCheckBox.IsChecked()


    @property
    def style (self):
        return self.styleComboBox.GetValue()


    def __createGui(self):
        """
        Создать элементы управления
        """
        mainSizer = wx.FlexGridSizer (0, 1)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableRow(3)

        self.__createFileGui (mainSizer)
        self.__createLanguageGui (mainSizer)
        self.__createStyleGui (mainSizer)
        self.__createTabWidthGui (mainSizer)
        self.__createOkCancelButtons (mainSizer)

        self.SetSizer(mainSizer)
        self.Layout()
        self.Fit()


    def __createOkCancelButtons (self, mainSizer):
        okCancel = self.CreateButtonSizer (wx.OK | wx.CANCEL)
        mainSizer.AddStretchSpacer()
        mainSizer.Add (
                okCancel,
                proportion=1,
                flag=wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM,
                border=2
                )


    def __createLanguageGui (self, mainSizer):
        """
        Создать интерфейс, связанный с языком программирования
        """
        langSizer = wx.FlexGridSizer (0, 2)
        langSizer.AddGrowableCol(1)

        languageLabel = wx.StaticText(self, -1, _(u"Language"))
        self.languageComboBox = wx.ComboBox (self, 
                style=wx.CB_DROPDOWN | wx.CB_READONLY)

        self.languageComboBox.SetMinSize (wx.Size (self._fieldsWidth, -1))

        langSizer.Add (
                languageLabel,
                proportion=1,
                flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                border=2
                )


        langSizer.Add (
                self.languageComboBox,
                proportion=1,
                flag=wx.ALL | wx.ALIGN_RIGHT,
                border=2
                )

        mainSizer.Add (
                langSizer, 
                proportion=1,
                flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND,
                border=2
                )


    def __createTabWidthGui (self, mainSizer):
        """
        Создать интерфейс, связанный с размером табуляции
        """
        tabSizer = wx.FlexGridSizer (0, 2)
        tabSizer.AddGrowableCol(1)

        tabWidthLabel = wx.StaticText(self, -1, _(u"Tab Width (0 - Default Value)"))
        self.tabWidthSpin = wx.SpinCtrl (
                self, 
                style=wx.SP_ARROW_KEYS|wx.TE_AUTO_URL
                )
        self.tabWidthSpin.SetMinSize (wx.Size (self._fieldsWidth, -1))


        tabSizer.Add (
                tabWidthLabel, 
                proportion=1,
                flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                border=2
                )

        tabSizer.Add (
                self.tabWidthSpin, 
                proportion=1,
                flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT,
                border=2
                )

        mainSizer.Add (
                tabSizer, 
                proportion=1,
                flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.EXPAND,
                border=2
                )


    def __createStyleGui (self, mainSizer):
        """
        Создать интерфейс, связанный с выбором стиля оформления
        """
        styleSizer = wx.FlexGridSizer (0, 2)
        styleSizer.AddGrowableCol(1)

        styleLabel = wx.StaticText(self, -1, _(u"Style"))
        self.styleComboBox = wx.ComboBox (self, 
                style=wx.CB_DROPDOWN | wx.CB_READONLY)

        self.styleComboBox.SetMinSize (wx.Size (self._fieldsWidth, -1))

        styleSizer.Add (
                styleLabel,
                proportion=1,
                flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                border=2
                )


        styleSizer.Add (
                self.styleComboBox,
                proportion=1,
                flag=wx.ALL | wx.ALIGN_RIGHT,
                border=2
                )

        mainSizer.Add (
                styleSizer, 
                proportion=1,
                flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND,
                border=2
                )


    def __createFileGui (self, mainSizer):
        """
        Создать интерфейс, связанный со вставкой исходников из вложенных файлов
        """
        self.fileCheckBox = wx.CheckBox (
                self,
                label = _(u"Insert source from file"))

        mainSizer.Add (
                self.fileCheckBox, 
                proportion=1,
                flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.EXPAND,
                border=2
                )

        fileSizer = wx.FlexGridSizer (0, 3)
        fileSizer.AddGrowableCol (2)

        # Список для выбора прикрепленных файлов
        self.attachmentLabel = wx.StaticText(self, -1, _(u"Attached file"))
        self.attachmentComboBox = wx.ComboBox (self,
                style=wx.CB_DROPDOWN | wx.CB_READONLY)

        self.attachmentComboBox.SetMinSize ((self._fieldsWidth, -1))

        fileSizer.Add ((self._indent, 0))

        fileSizer.Add (
                self.attachmentLabel, 
                proportion=1,
                flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                border=2
                )

        fileSizer.Add (
                self.attachmentComboBox, 
                proportion=1,
                flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT,
                border=2
                )

        # Выбор кодировки файла
        self.encodingLabel = wx.StaticText(self, -1, _(u"File encoding"))
        self.encodingComboBox = wx.ComboBox (self,
                style=wx.CB_DROPDOWN)

        self.encodingComboBox.SetMinSize ((self._fieldsWidth, -1))

        # Размер отступа
        fileSizer.Add ((self._indent, 0))

        fileSizer.Add (
                self.encodingLabel, 
                proportion=1,
                flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                border=2
                )

        fileSizer.Add (
                self.encodingComboBox, 
                proportion=1,
                flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT,
                border=2
                )

        mainSizer.Add (
                fileSizer, 
                proportion=1,
                flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.EXPAND,
                border=2
                )


