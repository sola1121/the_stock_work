# coding: utf-8
# producer: 王健吉(leimilia)

"""初次连接数据库并生成版本信息"""

import cx_Oracle
import sys

from tkinter import messagebox
from window_main import run_window_main

pointer = False

def link_database(trans):
    try:
        # 创建连接
        connection = cx_Oracle.connect(trans.user_name, trans.user_pwd, trans.database_address)
        # 创建游标
        cursor = connection.cursor()

        def show_version():
            cursor.execute("select * from v$version")
            versions = cursor.fetchall()
            ver = []
            for version in versions:
                ver.append('%s' %version)
            return ver

        trans.ver = show_version()

        global pointer
        pointer = True

    except:
        info = sys.exc_info()
        info1 = list(info)
        all_info = str(info1[1])
        messagebox.showerror(title='Error', message=all_info)

    if pointer:
        run_window_main(trans)


