# coding: utf-8
# producer: 王健吉(leimilia)

import tkinter as tk
from tkinter import messagebox

from window_main import run_window_main
from trans import Trans
from link_database import link_database

trans = Trans()

window_log = tk.Tk()
window_log.title('仓库管理登陆')
window_log.geometry('400x290+500+250')
window_log.resizable(width=False, height=False)

canvas = tk.Canvas(window_log, height=150, width=300) # 创建画布
image_file = tk.PhotoImage(file='images/yun.png') # 加载图片文件
image = canvas.create_image(0,0, anchor='nw', image=image_file)#将图片置于画布上
canvas.pack(side='top')

tk.Label(window_log, text='User name: ').place(x=60, y=160)
tk.Label(window_log, text='Password: ').place(x=60, y=200)

var_usr_name = tk.StringVar() # 定义变量
var_usr_name.set(trans.user_name) # 变量赋值
entry_usr_name = tk.Entry(window_log, textvariable=var_usr_name)
entry_usr_name.place(x=160, y=160)

var_usr_pwd = tk.StringVar() # 定义变量
entry_usr_pwd = tk.Entry(window_log, textvariable=var_usr_pwd, show='*')
entry_usr_pwd.place(x=160, y=200)

def usr_log():
    """登陆窗login_in方法"""
    trans.user_name = var_usr_name.get()
    trans.user_pwd = var_usr_pwd.get()
    link_database(trans)

def change_warehouse():
    """登陆窗change_warehouse方法"""
    toplevel = tk.Toplevel()
    toplevel.title('仓库数据库选择')
    toplevel.geometry('280x150+600+400')
    toplevel.resizable(0, 0)
    toplevel.wm_attributes("-topmost", 1)

    label1 = tk.Label(toplevel, text='主机名: ').place(x=40, y=10)
    label2 = tk.Label(toplevel, text='端口: ').place(x=40, y=40)
    label3 = tk.Label(toplevel, text='SID: ').place(x=40, y=70)

    var_localhost = tk.StringVar()
    var_localhost.set(trans.host)
    var_port = tk.StringVar()  # 定义变量
    var_port.set(trans.port)  # 变量赋值
    var_sid = tk.StringVar()
    var_sid.set(trans.sid)
    entry1 = tk.Entry(toplevel, textvariable=var_localhost).place(x=90, y=10)
    entry2 = tk.Entry(toplevel, textvariable=var_port).place(x=90, y=40)
    entry3 = tk.Entry(toplevel, textvariable=var_sid).place(x=90, y=70)

    def change():
        """副窗更改数据库连接方法"""
        trans.host = var_localhost.get()
        trans.port = var_port.get()
        trans.sid = var_sid.get()
        trans.database_address = trans.get_database_address()
        toplevel.withdraw()

    button1 = tk.Button(toplevel, text='Confirm', command=change).place(x=50, y=100)
    button2 = tk.Button(toplevel, text='GoBack', command=toplevel.withdraw).place(x=170, y=100)
    toplevel.mainloop()

btn_login = tk.Button(window_log, text='Login in', width=10, command=usr_log)
btn_login.place(x=100 , y=240)

btn_warehouse = tk.Button(window_log, text='Warehouse', width=10, command=change_warehouse)
btn_warehouse.place(x=230, y=240)

# 制作人
tk.Label(window_log, text='by 王健吉(leimilia)', font=('黑体', 6)).place(x=320, y=275)

window_log.mainloop()
