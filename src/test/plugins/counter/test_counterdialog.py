# -*- coding: UTF-8 -*-

import wx

from outwiker.core.application import Application
from outwiker.core.pluginsloader import PluginsLoader
from outwiker.pages.wiki.wikipage import WikiPageFactory

from test.guitests.basemainwnd import BaseMainWndTest
from outwiker.gui.tester import Tester


class CounterDialogTest (BaseMainWndTest):
    """
    Тесты диалога для плагина Counter
    """
    def setUp (self):
        BaseMainWndTest.setUp (self)

        self.filesPath = u"../test/samplefiles/"
        WikiPageFactory().create (self.wikiroot, u"Страница 1", [])

        dirlist = [u"../plugins/counter"]

        self._loader = PluginsLoader(Application)
        self._loader.load (dirlist)

        from counter.insertdialog import InsertDialog
        self._dlg = InsertDialog (Application.mainWindow)
        Tester.dialogTester.clear()
        Tester.dialogTester.appendOk()

        self.testPage = self.wikiroot[u"Страница 1"]


    def tearDown(self):
        Application.wikiroot = None
        self._dlg.Destroy()
        self._loader.clear()

        BaseMainWndTest.tearDown (self)


    def testDefault (self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController (
            self._dlg,
            Application.config,
            self.testPage)

        result = controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual (result, wx.ID_OK)
        self.assertEqual (self._dlg.counterName, u"")
        self.assertEqual (self._dlg.parentName, u"")
        self.assertEqual (self._dlg.separator, u".")
        self.assertEqual (self._dlg.reset, False)
        self.assertEqual (self._dlg.start, 1)
        self.assertEqual (self._dlg.step, 1)
        self.assertEqual (self._dlg.hide, False)
        self.assertEqual (self._dlg.countersList, [u""])

        self.assertEqual (text, u'(:counter:)')


    def testDestroy (self):
        Application.wikiroot = None
        self._loader.clear()


    def testSetEmptyName_01 (self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController (self._dlg,
                                             Application.config,
                                             self.testPage)

        self._dlg.counterName = u""

        controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual (text, u'(:counter:)')


    def testSetEmptyName_02 (self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController (self._dlg,
                                             Application.config,
                                             self.testPage)

        self._dlg.counterName = u"    "

        controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual (text, u'(:counter:)')


    def testSetName (self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController (self._dlg,
                                             Application.config,
                                             self.testPage)

        self._dlg.counterName = u"Имя счетчика"

        controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual (text, u'(:counter name="Имя счетчика":)')


    def testSetParentEmptyName_01 (self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController (self._dlg,
                                             Application.config,
                                             self.testPage)

        self._dlg.parentName = u""

        controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual (text, u'(:counter:)')


    def testSetParentEmptyName_02 (self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController (self._dlg,
                                             Application.config,
                                             self.testPage)

        self._dlg.parentName = u"     "

        controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual (text, u'(:counter:)')


    def testSetParentName (self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController (self._dlg,
                                             Application.config,
                                             self.testPage)

        self._dlg.parentName = u"Имя счетчика"

        controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual (text, u'(:counter parent="Имя счетчика":)')


    def testSetSeparatorDefault (self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController (self._dlg,
                                             Application.config,
                                             self.testPage)

        self._dlg.separator = u"."

        controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual (text, u'(:counter:)')


    def testSetSeparatorWithoutParent (self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController (self._dlg,
                                             Application.config,
                                             self.testPage)

        self._dlg.separator = u":"

        controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual (text, u'(:counter:)')


    def testSetSeparatorWithParent_01 (self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController (self._dlg,
                                             Application.config,
                                             self.testPage)

        self._dlg.separator = u":"
        self._dlg.parentName = u"Родительский счетчик"

        controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual (text, u'(:counter parent="Родительский счетчик" separator=":":)')


    def testNotReset_01 (self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController (self._dlg,
                                             Application.config,
                                             self.testPage)

        self._dlg.reset = False
        self._dlg.start = 0

        controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual (text, u'(:counter:)')


    def testNotReset_02 (self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController (self._dlg,
                                             Application.config,
                                             self.testPage)

        self._dlg.reset = False
        self._dlg.start = 100

        controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual (text, u'(:counter:)')


    def testReset_01 (self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController (self._dlg,
                                             Application.config,
                                             self.testPage)

        self._dlg.reset = True
        self._dlg.start = 0

        controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual (text, u'(:counter start=0:)')


    def testReset_02 (self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController (self._dlg,
                                             Application.config,
                                             self.testPage)

        self._dlg.reset = True
        self._dlg.start = -10

        controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual (text, u'(:counter start=-10:)')


    def testReset_03 (self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController (self._dlg,
                                             Application.config,
                                             self.testPage)

        self._dlg.reset = True
        self._dlg.start = 1

        controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual (text, u'(:counter start=1:)')


    def testReset_04 (self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController (self._dlg,
                                             Application.config,
                                             self.testPage)

        self._dlg.reset = True
        self._dlg.start = 10

        controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual (text, u'(:counter start=10:)')


    def testStep_01 (self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController (self._dlg,
                                             Application.config,
                                             self.testPage)

        self._dlg.step = 1
        controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual (text, u'(:counter:)')


    def testStep_02 (self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController (self._dlg,
                                             Application.config,
                                             self.testPage)

        self._dlg.step = 0
        controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual (text, u'(:counter step=0:)')


    def testStep_03 (self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController (self._dlg,
                                             Application.config,
                                             self.testPage)

        self._dlg.step = -10
        controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual (text, u'(:counter step=-10:)')


    def testStep_04 (self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController (self._dlg,
                                             Application.config,
                                             self.testPage)

        self._dlg.step = 10
        controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual (text, u'(:counter step=10:)')


    def testHide_01 (self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController (self._dlg,
                                             Application.config,
                                             self.testPage)

        self._dlg.hide = False
        controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual (text, u'(:counter:)')


    def testHide_02 (self):
        from counter.insertdialogcontroller import InsertDialogController

        controller = InsertDialogController (self._dlg,
                                             Application.config,
                                             self.testPage)

        self._dlg.hide = True
        controller.showDialog()
        text = controller.getCommandString()

        self.assertEqual (text, u'(:counter hide:)')


    def testCountersList_01 (self):
        self.testPage.content = u'''(:counter:)'''

        from counter.insertdialogcontroller import InsertDialogController

        InsertDialogController (self._dlg, Application.config, self.testPage)

        self.assertEqual (self._dlg.countersList, [u""])


    def testCountersList_02 (self):
        self.testPage.content = u'''(:counter name="Счетчик":)'''

        from counter.insertdialogcontroller import InsertDialogController

        InsertDialogController (self._dlg, Application.config, self.testPage)

        self.assertEqual (self._dlg.countersList, [u"", u"Счетчик"])


    def testCountersList_03 (self):
        self.testPage.content = u'''(:counter name="Счетчик":) (:counter name="Счетчик":)'''

        from counter.insertdialogcontroller import InsertDialogController

        InsertDialogController (self._dlg, Application.config, self.testPage)

        self.assertEqual (self._dlg.countersList, [u"", u"Счетчик"])


    def testCountersList_04 (self):
        self.testPage.content = u'''(:counter name="Счетчик":) (:counter name="Абырвалг   ":)'''

        from counter.insertdialogcontroller import InsertDialogController

        InsertDialogController (self._dlg, Application.config, self.testPage)

        self.assertEqual (self._dlg.countersList, [u"", u"Абырвалг", u"Счетчик"])


    def testCountersList_05 (self):
        self.testPage.content = u'''(:counter name="Счетчик":) (:counter name='Абырвалг':) (:counter name="":)'''

        from counter.insertdialogcontroller import InsertDialogController

        InsertDialogController (self._dlg, Application.config, self.testPage)

        self.assertEqual (self._dlg.countersList, [u"", u"Абырвалг", u"Счетчик"])


    def testCountersList_06 (self):
        self.testPage.content = u'''(:counter name="Счетчик":) (:counter name=Абырвалг:) (:counter name="":)'''

        from counter.insertdialogcontroller import InsertDialogController

        InsertDialogController (self._dlg, Application.config, self.testPage)

        self.assertEqual (self._dlg.countersList, [u"", u"Абырвалг", u"Счетчик"])
