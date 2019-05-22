#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import xlrd,time,sys,unittest    #导入xlrd等相关模块
# class Data_Excel(unittest.TestCase):# 封装在Data_Excel类里面方便后面使用
#     file_addrec = r'C:\Users\liqiang22230\Desktop\date.xlsx' #定义date.xlsx数据维护Excel的路径文件
#     def open_excel(self,file = file_addrec):#file = file_addrec #注意在class中def中一定要带self
#         try:#检验文件有没有被获取到
#             self.data =xlrd.open_workbook(file)
#             return self.data
#         except Exception :
#             print(file)
#             print('eero')
#     def excel_table_byindex(self,file = file_addrec,colnameindex=0,by_index='用户表'):
#         #把这个读取Excel中封装在excel_table_byindex函数中，这时需要三个参数1.文件2.sheet名称，列所在的行数
#         self.data = xlrd.open_workbook(file)#获取Excel数据
#         self.table = self.data.sheet_by_name(by_index)#使用sheet_by_name获取sheet页名叫用户表的sheet对象数据
#         self.colnames  = self.table.row_values(colnameindex)#获取行数下标为0也就是第一行Excel中第一行的所有的数据值
#         self.nrows = self.table.nrows #获得所有的有效行数
#         list = []#总体思路是把Excel中数据以字典的形式存在字符串中一个字典当成一个列表元素
#         for rownum in range(1,self.nrows):
#             row = self.table.row_values(rownum)#获取所有行数每一行的数据值
#             if row:
#                 app = {}#主要以{'name': 'zhangsan', 'password': 12324.0}，至于字典中有多少元素主要看有多少列
#                 for i in range(len(self.colnames)):
#         #在这个Excel中，列所在的行有两个数据，所以没循环一行就以这两个数据为键，行数的值为键的值，保存在一个字典里
#                     app[self.colnames[i]] = row[i]
#                     list.append(app)
#         print(list)
#         return list
# a = Data_Excel()
# a.excel_table_byindex()
# if __name__=="__main__":
#     unittest.main()


data = xlrd.open_workbook('dtest.xlsx')
table = data.sheets()[0]
print(data.sheet_names())
nrows = table.nrows
for i in range(nrows):
    # for j in range(table.ncols):
    #     print('{}行{}列'.format(i,j))
    #     print(type(table.cell_value(i, j)))
    print(table.row_values(i, start_colx=0, end_colx=None))