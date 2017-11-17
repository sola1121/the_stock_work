# coding: utf-8
# producer: 王健吉(leimilia)

import cx_Oracle
import sys

from tkinter import messagebox

class LinkDatabase():
    def __init__(self, trans):
        self.pointer = False
        self.trans = trans
        self.connection = None
        self.cursor = None
        self.info = None

    def conn(self):
        try:
            self.connection = cx_Oracle.connect(self.trans.user_name, self.trans.user_pwd, self.trans.database_address)
            self.cursor = self.connection.cursor()
        except:
            self.info = sys.exc_info()
            messagebox.showerror(title='Error', message=self.info)

    def get_row(self):
        return self.cursor.rowcount

    def get_head(self):
        x = ''
        head = self.cursor.description
        title = [i[0] for i in head]
        # 格式化字符串
        g = lambda k: "%-8s" % k
        title = map(g, title)
        for i in title:
            x += str(i) + '  '
        return x

    def select(self, sql):
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results

    def select_para(self, sql, para):
        self.cursor.execute(sql, para)
        results = self.cursor.fetchall()
        return results

    def insert_update_para(self, sql, para):
        self.cursor.execute(sql, para)
        self.cursor.execute('commit')
        return self.cursor

    def close_conn(self):
        self.cursor.close()
        self.connection.close()


"""
    def DMLDB_N(sql):
        ##插入，更新，删除
        self.cursor.execute(sql)
        cursor.close()
        db.commit()

    def DMLDB_P(db, sql, para):
        ##插入，更新，删除
        cursor = db.cursor()
        cursor.execute(sql, para)
        cursor.close()
        db.commit()

    def DDLDB(db, sql):
        # DDL 语句
        cursor = db.cursor()
        cursor.execute(sql)
        cursor.close()

    def printResult(rs):
        for row in rs:
            print
            row
"""
