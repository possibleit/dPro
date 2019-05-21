#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import xlrd
from dPro.settings import BASE_DIR
def parse(file_path):
    file = xlrd.open_workbook(file_path)
    sheet_1 = file.sheet_by_index(0)
    row_num = sheet_1.nrows #获取行数
    for i in range(0,row_num): #循环每一行数据
        row = sheet_1.row_values(i) #获取行数据
        dict = {}
        dict['name']= "".join(row[0]) #姓名

        print(dict)

parse(BASE_DIR + '\\test.xlsx')
