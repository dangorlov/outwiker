#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from libs.pyparsing import Regex, OneOrMore, Optional, LineEnd, LineStart
from utils import replaceBreakes


class TableFactory (object):
	@staticmethod
	def make (parser):
		return TableToken(parser).getToken()


class TableToken (object):
	"""
	Токен для таблиц
	"""
	def __init__ (self, parser):
		self.parser = parser


	def getToken (self):
		tableCell = Regex ("(?P<text>.*?)\\|\\|")
		tableCell.setParseAction(self.__convertTableCell)

		tableRow = LineStart() + "||" + OneOrMore (tableCell) + Optional (LineEnd())
		tableRow.setParseAction(self.__convertTableRow)

		table = LineStart() + Regex ("\\|\\| *(?P<params>.+)?") + LineEnd() + OneOrMore (tableRow)
		table.setParseAction(self.__convertTable)

		return table


	def __convertTableCell (self, s, loc, toks):
		text = toks["text"]

		leftAlign = toks["text"][-1] in " \t"
		
		# Условие в скобках связано с тем, что первый пробел попадает 
		# или не попадает в токен в зависимости от того, первая ячейка в строке или первая ячейка в строке или нет
		rightAlign = loc > 0 and (s[loc - 1] in " \t" or s[loc] in " \t")

		align = u''

		if leftAlign and rightAlign:
			align = u' ALIGN="CENTER"'
		elif leftAlign:
			align = u' ALIGN="LEFT"'
		elif rightAlign:
			align = u' ALIGN="RIGHT"'

		result = u'<TD%s>%s</TD>' % (align, self.parser.wikiMarkup.transformString (replaceBreakes (text.strip() ) ) )

		return result


	def __convertTableRow (self, s, l, t):
		if t[-1] == "\n":
			lastindex = len (t) - 1
		else:
			lastindex = len (t)

		result = u"<TR>"
		for n in range (1, lastindex):
			result += t[n]

		result += "</TR>"

		return result


	def __convertTable (self, s, l, t):
		result = u"<TABLE %s>" % t[0][2:].strip()
		for n in range (2, len (t)):
			result += t[n]

		result += "</TABLE>"

		return result
