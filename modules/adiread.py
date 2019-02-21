#-*- coding:utf-8 -*-
import xlrd
from modules.database_controller.Mongodb import *

def adi():
    a = MongoDB('80.7.238.136', 8889, 'testposeidon', 'adi', 'root', 'qwert789')
    book = xlrd.open_workbook('/tmp/20190109.xls')
    sheet = book.sheet_by_index(0)
    name = []
    rows = sheet.nrows
    for i in range(28):
        name.append(sheet.cell(0,i).value)

    for x in range(1,rows):
        cols = []
        for y in range(28):
            cols.append(sheet.cell(x,y).value)
        test = dict(zip(name,cols))
        a.insert(test, 'one')
