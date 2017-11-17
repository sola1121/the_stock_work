# coding: utf-8
# producer: 王健吉(leimilia)

import tkinter
import sys

from tkinter import messagebox
from class_data import LinkDatabase
from terminal import terminal
from terminal_os_system import terminal_os

from SQL_query import *

def run_window_main(trans):

    link = LinkDatabase(trans)
    # 主窗口是一个toplevel
    window_main = tkinter.Toplevel()
    window_main.title('主控制界面')
    window_main.geometry('870x515')
    window_main.resizable(0, 0)

    # 按钮图标
    img_terminal = tkinter.PhotoImage(file='images/terminal.png')

    img_show_data_pur = tkinter.PhotoImage(file='images/purchase_order.png')
    img_show_data_warehouse = tkinter.PhotoImage(file='images/warehouse.png')
    img_show_date_customer_order = tkinter.PhotoImage(file='images/customer_order.png')
    img_show_data_customer = tkinter.PhotoImage(file='images/customer.png')

    # 登陆用户名
    tkinter.Label(window_main, text='当前用户: ' + str(trans.user_name)).place(x=0, y=0)

    # label用于计行数
    var_count = tkinter.StringVar()
    tkinter.Label(window_main, textvariable=var_count, bg='white', width=10).place(x=215, y=2)

    # 创建显示表头的label
    var_header = tkinter.StringVar()
    var_header.set('Database_version')
    header_label = tkinter.Label(window_main, width=80, textvariable=var_header, bg='green', anchor='w').place(x=290, y=2)

    # 创建主list和滑动条
    mylist = tkinter.Listbox(window_main, width=80, height=26)

    scrollbar_y = tkinter.Scrollbar(window_main)
    scrollbar_y.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    scrollbar_x = tkinter.Scrollbar(window_main, orient='horizontal')
    scrollbar_x.pack(side=tkinter.BOTTOM, fill='x')

    mylist.config(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)
    mylist.place(x=290, y=25)
    scrollbar_x.config(command=mylist.xview)
    scrollbar_y.config(command=mylist.yview)

    for version in trans.ver:   # 得到数据库版本信息
        mylist.insert(tkinter.END, str(version))

    def into_head_label(value):
        """更新表头"""
        var_header.set(value)

    def into_mylist(value):
        """更新list"""
        mylist.insert('end', value)

    def run_terminal():
        terminal(trans) # 自制的数据库终端
        # 或 terminal_os()

    # 采购订单的方法们
    def select_pur():
        """输出所有采购订单"""
        try:
            mylist.delete(0, 'end')   # 清空list
            link.conn()
            results = link.select(sql_select_pur)
            for result in results:
                into_mylist(result)
            into_head_label(link.get_head())
            var_count.set(str(link.get_row()) + ' rows')   # 得到结果行数
            link.close_conn()
        except:
            info = sys.exc_info()
            info1 = list(info)
            all_info = str(info1[1])
            messagebox.showerror(title='Error', message=all_info)

    def insert_pur_ware():
        """将采购订单入库"""
        re_stock, re_date, re_costs, re_clerk = '', '当前时间', '', ''

        change_top = tkinter.Toplevel()
        change_top.title('采购入库')
        change_top.geometry('280x280+600+400')
        change_top.resizable(0, 0)

        # 提示用户ID的label
        tkinter.Label(change_top, text='输入采购单号: ').place(x=20, y=10)
        var_id = tkinter.StringVar()
        var_id.set('请输入采购id')
        tkinter.Entry(change_top, textvariable=var_id, width=15).place(x=100, y=10)

        label1 = tkinter.Label(change_top, text='库存编号：').place(x=30, y=60)
        label2 = tkinter.Label(change_top, text='入库时间：').place(x=30, y=90)
        label3 = tkinter.Label(change_top, text='在库成本：').place(x=30, y=120)
        label4 = tkinter.Label(change_top, text='库存负责人：').place(x=30, y=150)
        label5 = tkinter.Label(change_top, text='入库数量：').place(x=30, y=180)

        var_stock = tkinter.StringVar()
        var_stock.set(re_stock)
        var_date = tkinter.StringVar()  # 定义变量
        var_date.set(re_date)
        var_costs = tkinter.DoubleVar()
        var_costs.set(re_costs)
        var_clerk = tkinter.StringVar()
        var_clerk.set(re_clerk)
        var_quan = tkinter.IntVar()
        var_quan.set(0)

        entry1 = tkinter.Entry(change_top, textvariable=var_stock).place(x=110, y=60)
        entry2 = tkinter.Entry(change_top, textvariable=var_date).place(x=110, y=90)
        entry3 = tkinter.Entry(change_top, textvariable=var_costs).place(x=110, y=120)
        entry4 = tkinter.Entry(change_top, textvariable=var_clerk).place(x=110, y=150)
        entry5 = tkinter.Entry(change_top, textvariable=var_quan).place(x=110, y=180)

        def check_id():
            try:
                link.conn()
                purchase_id = var_id.get().strip().upper()
                status = link.select_para(sql_pur8, (purchase_id,))
                result = link.select_para(sql_pur1, (purchase_id,))
                if result and ('0' in str(status)):
                    var_id.set(purchase_id)
                else:
                    messagebox.showwarning(title='警告', message='订单不存在,或已入库.')
                link.close_conn()
            except:
                info = sys.exc_info()
                info1 = list(info)
                all_info = str(info1[1])
                messagebox.showerror(title='Error', message=all_info)

        def insert_stock():
            try:
                purchase_id = var_id.get().strip().upper()
                link.conn()
                if var_date.get() == '当前时间':
                    para = {
                        'stock_id': str(var_stock.get()),
                        'pur_id': purchase_id,
                        'costs': str(var_costs.get()),
                        'clerk': str(var_clerk.get()),
                        'quantity': int(var_quan.get()),
                    }
                    print(para)
                    results = link.insert_update_para(sql_pur_ware2, para)
                    if results:
                        link.insert_update_para(sql_pur_status, (purchase_id,))
                        messagebox.showinfo(title='提示', message='添加完成')
                else:
                    para = {
                        'stock_id': str(var_stock.get()),
                        'pur_id': purchase_id,
                        'en_date': str(var_date.get()),
                        'costs': str(var_costs.get()),
                        'clerk': str(var_clerk.get()),
                        'quantity': int(var_quan.get()),
                    }
                    results = link.insert_update_para(sql_pur_ware1, para)
                    if results:
                        link.insert_update_para(sql_pur_status, (purchase_id,))
                        messagebox.showinfo(title='提示', message='添加完成')
                link.close_conn()
            except:
                info = sys.exc_info()
                info1 = list(info)
                all_info = str(info1[1])
                messagebox.showerror(title='Error', message=all_info)

        btn_uid = tkinter.Button(change_top, text='Checked', font=('Consolas', 8), command=check_id).place(x=220, y=10)
        btn_confirm = tkinter.Button(change_top, text="Confirm", command=insert_stock).place(x=50, y=240)
        btn_back = tkinter.Button(change_top, text='Back', command=change_top.withdraw).place(x=170, y=240)

    def search_pur():
        """采购订单的查询"""
        search_top = tkinter.Toplevel()
        search_top.title('查询采购订单信息')
        search_top.geometry('280x180+600+400')
        search_top.resizable(0, 0)
        search_top.wm_attributes("-topmost", 1)

        label1 = tkinter.Label(search_top, text='采购时间：').place(x=20, y=10)
        label2 = tkinter.Label(search_top, text='采购责任人：').place(x=20, y=40)
        label3 = tkinter.Label(search_top, text='采购服装品牌：').place(x=20, y=70)

        var_date = tkinter.StringVar()
        var_date.set('')
        var_liable = tkinter.StringVar()  # 定义变量
        var_liable.set('')  # 变量赋值
        var_brand = tkinter.StringVar()
        var_brand.set('')
        entry1 = tkinter.Entry(search_top, textvariable=var_date).place(x=110, y=10)
        entry2 = tkinter.Entry(search_top, textvariable=var_liable).place(x=110, y=40)
        entry3 = tkinter.Entry(search_top, textvariable=var_brand).place(x=110, y=70)

        ck1_num = tkinter.IntVar()
        ck1_num.set(1)
        ck2_num = tkinter.IntVar()
        ck2_num.set(1)

        ck1 = tkinter.Checkbutton(search_top, text='已入库', variable=ck1_num, onvalue=1, offvalue=0).place(x=60, y=100)
        ck1 = tkinter.Checkbutton(search_top, text='未入库', variable=ck2_num, onvalue=1, offvalue=0).place(x=160, y=100)

        def select_where():
            try:
                mylist.delete(0, 'end')
                if ck2_num==1 and ck1_num==1:
                    link.conn()
                    para = {
                        'time': '%'+str(var_date.get())+'%',
                        'duty': '%'+str(var_liable.get())+'%',
                        'brand': '%'+str(var_brand.get())+'%',
                        'status': '%',
                    }
                    results = link.select_para(sql_search_pur, para)
                    for result in results:
                        into_mylist(result)
                    into_head_label(link.get_head())  # 改变表头
                    var_count.set(str(link.get_row()) + ' rows')  # 得到结果行数
                    link.close_conn()
                elif ck2_num==0 and ck1_num==1:
                    link.conn()
                    para = {
                        'time': '%'+str(var_date.get())+'%',
                        'duty': '%'+str(var_liable.get())+'%',
                        'brand': '%'+str(var_brand.get())+'%',
                        'status': str(1),
                    }
                    results = link.select_para(sql_search_pur, para)
                    for result in results:
                        into_mylist(result)
                    into_head_label(link.get_head())  # 改变表头
                    var_count.set(str(link.get_row()) + ' rows')  # 得到结果行数
                    link.close_conn()
                elif ck2_num==1 and ck1_num==0:
                    link.conn()
                    para = {
                        'time': '%'+str(var_date.get())+'%',
                        'duty': '%'+str(var_liable.get())+'%',
                        'brand': '%'+str(var_brand.get())+'%',
                        'status': str(0),
                    }
                    results = link.select_para(sql_search_pur, para)
                    for result in results:
                        into_mylist(result)
                    into_head_label(link.get_head())  # 改变表头
                    var_count.set(str(link.get_row()) + ' rows')  # 得到结果行数
                    link.close_conn()
                else:
                    link.conn()
                    para = {
                        'time': '%' + str(var_date.get()) + '%',
                        'duty': '%' + str(var_liable.get()) + '%',
                        'brand': '%' + str(var_brand.get()) + '%',
                        'status': '%',
                    }
                    results = link.select_para(sql_search_pur, para)
                    for result in results:
                        into_mylist(result)
                    into_head_label(link.get_head())  # 改变表头
                    var_count.set(str(link.get_row()) + ' rows')  # 得到结果行数
                    link.close_conn()
            except:
                info = sys.exc_info()
                info1 = list(info)
                all_info = str(info1[1])
                messagebox.showerror(title='Error', message=all_info)

        btn_confirm = tkinter.Button(search_top, text="Confirm", command=select_where).place(x=50, y=130)
        btn_back = tkinter.Button(search_top, text='Back', command=search_top.withdraw).place(x=170, y=130)

    def insert_pur():
        """插入采购订单"""

        insert_top = tkinter.Toplevel()
        insert_top.title('添加采购订单')
        insert_top.geometry('280x270+600+400')
        insert_top.resizable(0, 0)

        label1 = tkinter.Label(insert_top, text='订单编号：').place(x=20, y=10)
        label2 = tkinter.Label(insert_top, text='采购时间：').place(x=20, y=40)
        label3 = tkinter.Label(insert_top, text='采购金额：').place(x=20, y=70)
        label4 = tkinter.Label(insert_top, text='采购商：').place(x=20, y=100)
        label5 = tkinter.Label(insert_top, text='服装种类：').place(x=20, y=130)
        label6 = tkinter.Label(insert_top, text='服装品牌：').place(x=20, y=160)
        label7 = tkinter.Label(insert_top, text='采购数量：').place(x=20, y=190)

        var_pur_id = tkinter.StringVar()  # 定义变量
        var_pur_id.set('')
        var_pur_date = tkinter.StringVar()
        var_pur_date.set('当前时间')
        var_price = tkinter.DoubleVar()
        var_price.set(0.0)
        var_agent = tkinter.StringVar()
        var_agent.set('')
        var_category = tkinter.StringVar()
        var_category.set('')
        var_brand = tkinter.StringVar()
        var_brand.set('')
        var_quantity = tkinter.IntVar()
        var_quantity.set(0)

        entry1 = tkinter.Entry(insert_top, textvariable=var_pur_id).place(x=110, y=10)
        entry2 = tkinter.Entry(insert_top, textvariable=var_pur_date).place(x=110, y=40)
        entry3 = tkinter.Entry(insert_top, textvariable=var_price).place(x=110, y=70)
        entry4 = tkinter.Entry(insert_top, textvariable=var_agent).place(x=110, y=100)
        entry5 = tkinter.Entry(insert_top, textvariable=var_category).place(x=110, y=130)
        entry6 = tkinter.Entry(insert_top, textvariable=var_brand).place(x=110, y=160)
        entry7 = tkinter.Entry(insert_top, textvariable=var_quantity).place(x=110, y=190)

        def select_where():
            try:
                mylist.delete(0, 'end')
                link.conn()
                if var_pur_date.get() == '当前时间':
                    para = {
                        'pur_id': str(var_pur_id.get()),
                        'price': float(var_price.get()),
                        'agent': str(var_agent.get()),
                        'category': str(var_category.get()),
                        'brand': str(var_brand.get()),
                        'quantity': int(var_quantity.get())
                    }
                    print(para)
                    results = link.insert_update_para(sql_insert_pur2, para)
                    if results:
                        messagebox.showinfo(title='提示', message='添加完成')
                else:
                    para = {
                        'pur_id': str(var_pur_id.get()),
                        'pur_date': var_pur_date.get(),
                        'price': float(var_price.get()),
                        'agent': str(var_agent.get()),
                        'category': str(var_category.get()),
                        'brand': str(var_brand.get()),
                        'quantity': int(var_quantity.get())
                    }
                    results = link.insert_update_para(sql_insert_pur1, para)
                    if results:
                        messagebox.showinfo(title='提示', message='添加完成')
                link.close_conn()
            except:
                info = sys.exc_info()
                info1 = list(info)
                all_info = str(info1[1])
                messagebox.showerror(title='Error', message=all_info)

        btn_confirm = tkinter.Button(insert_top, text="Confirm", command=select_where).place(x=50, y=220)
        btn_back = tkinter.Button(insert_top, text='Back', command=insert_top.withdraw).place(x=170, y=220)

    def update_pur():
        """更改订单"""
        re_date, re_price, re_agent, re_category, re_brand, re_quantity = '', '', '', '', '', ''

        change_top = tkinter.Toplevel()
        change_top.title('更改采购订单')
        change_top.geometry('280x290+600+400')
        change_top.resizable(0, 0)
        change_top.wm_attributes("-topmost", 1)

        # 提示用户ID的label
        tkinter.Label(change_top, text='输入采购单号: ').place(x=20, y=10)
        var_id = tkinter.StringVar()
        var_id.set('请输入采购id')
        tkinter.Entry(change_top, textvariable=var_id, width=15).place(x=100, y=10)

        label1 = tkinter.Label(change_top, text='采购时间：').place(x=30, y=60)
        label2 = tkinter.Label(change_top, text='采购金额：').place(x=30, y=90)
        label3 = tkinter.Label(change_top, text='采购商：').place(x=30, y=120)
        label4 = tkinter.Label(change_top, text='采购种类').place(x=30, y=150)
        label5 = tkinter.Label(change_top, text='采购品牌：').place(x=30, y=180)
        label6 = tkinter.Label(change_top, text='数量：').place(x=30, y=210)

        var_date = tkinter.StringVar()  # 定义变量
        var_date.set(re_date)
        var_price = tkinter.DoubleVar()
        var_price.set(re_price)
        var_agent = tkinter.StringVar()
        var_agent.set(re_agent)
        var_category = tkinter.StringVar()
        var_category.set(re_category)
        var_brand = tkinter.StringVar()
        var_brand.set(re_brand)
        var_quantity = tkinter.IntVar()
        var_quantity.set(re_quantity)

        entry1 = tkinter.Entry(change_top, textvariable=var_date).place(x=100, y=60)
        entry2 = tkinter.Entry(change_top, textvariable=var_price).place(x=100, y=90)
        entry3 = tkinter.Entry(change_top, textvariable=var_agent).place(x=100, y=120)
        entry4 = tkinter.Entry(change_top, textvariable=var_category).place(x=100, y=150)
        entry5 = tkinter.Entry(change_top, textvariable=var_brand).place(x=100, y=180)
        entry6 = tkinter.Entry(change_top, textvariable=var_quantity).place(x=100, y=210)

        def check_uid():
                link.conn()
                re_date = link.select_para(sql_pur2, (var_id.get(),))
                re_price = link.select_para(sql_pur3, (var_id.get(),))
                re_agent = link.select_para(sql_pur4, (var_id.get(),))
                re_category = link.select_para(sql_pur5, (var_id.get(),))
                re_brand = link.select_para(sql_pur6, (var_id.get(),))
                re_quantity = link.select_para(sql_pur7, (var_id.get(),))

                var_date.set(re_date)
                var_price.set(re_price)
                var_agent.set(re_agent)
                var_category.set(re_category)
                var_brand.set(re_brand)
                var_quantity.set(re_quantity)

                link.close_conn()

        def change_info():
            try:
                para = {
                    'pur_id': str(var_id.get()).strip(),
                    'pur_date': str(var_date.get()).strip(),
                    'pur_price': float(var_price.get()),
                    'pur_agent': str(var_agent.get()).strip(),
                    'pur_category': str(var_category.get()).strip(),
                    'pur_brand': str(var_brand.get()).strip(),
                    'pur_quantity': int(var_quantity.get())
                }
                link.conn()
                result = link.insert_update_para(sql_update_pur, para)
                if result:
                    messagebox.showinfo(title='提示', message='更改成功')
                link.close_conn()
            except:
                info = sys.exc_info()
                info1 = list(info)
                all_info = str(info1[1])
                messagebox.showerror(title='Error', message=all_info)

        btn_uid = tkinter.Button(change_top, text='Checked', font=('Consolas', 8), command=check_uid).place(x=220, y=10)
        btn_confirm = tkinter.Button(change_top, text="Confirm", command=change_info).place(x=50, y=240)
        btn_back = tkinter.Button(change_top, text='Back', command=change_top.withdraw).place(x=170, y=240)


    # 仓库的方法们
    def select_ware():
        """显示所有仓储物品"""
        try:
            mylist.delete(0, 'end')  # 清空list
            link.conn()
            results = link.select(sql_select_ware)
            for result in results:
                into_mylist(result)
            into_head_label(link.get_head())
            var_count.set(str(link.get_row()) + ' rows')  # 得到结果行数
            link.close_conn()
        except:
            info = sys.exc_info()
            info1 = list(info)
            all_info = str(info1[1])
            messagebox.showerror(title='Error', message=all_info)

    def search_ware():
        """查询仓库物品"""

        search_top = tkinter.Toplevel()
        search_top.title('查询仓储物品')
        search_top.geometry('280x210+600+400')
        search_top.resizable(0, 0)
        search_top.wm_attributes("-topmost", 1)

        label1 = tkinter.Label(search_top, text='仓储编号名：').place(x=20, y=10)
        label2 = tkinter.Label(search_top, text='采购单号：').place(x=20, y=40)
        label3 = tkinter.Label(search_top, text='入库时间：').place(x=20, y=70)
        label4 = tkinter.Label(search_top, text='储存物总价：').place(x=20, y=100)
        label5 = tkinter.Label(search_top, text='仓库负责人：').place(x=20, y=130)

        var_id = tkinter.StringVar()  # 定义变量
        var_id.set('')
        var_pur = tkinter.StringVar()
        var_pur.set('')
        var_date = tkinter.StringVar()
        var_date.set('')
        var_cost = tkinter.StringVar()
        var_cost.set('')
        var_clerk = tkinter.StringVar()
        var_clerk.set('')

        entry1 = tkinter.Entry(search_top, textvariable=var_id).place(x=110, y=10)
        entry2 = tkinter.Entry(search_top, textvariable=var_pur).place(x=110, y=40)
        entry3 = tkinter.Entry(search_top, textvariable=var_date).place(x=110, y=70)
        entry4 = tkinter.Entry(search_top, textvariable=var_cost).place(x=110, y=100)
        entry5 = tkinter.Entry(search_top, textvariable=var_clerk).place(x=110, y=130)

        def select_where():
            try:
                mylist.delete(0, 'end')
                link.conn()
                para = {
                    'stock': '%' + str(var_id.get()) + '%',
                    'purchase': '%' + str(var_pur.get()) + '%',
                    'en_date': '%' + str(var_date.get()) + '%',
                    'costs': '%' + str(var_cost.get()) + '%',
                    'clerk': '%' + str(var_clerk.get()) + '%'
                }
                results = link.select_para(sql_search_ware, para)
                for result in results:
                    into_mylist(result)
                into_head_label(link.get_head())  # 改变表头
                var_count.set(str(link.get_row()) + ' rows')  # 得到结果行数
                link.close_conn()
            except:
                info = sys.exc_info()
                info1 = list(info)
                all_info = str(info1[1])
                messagebox.showerror(title='Error', message=all_info)

        btn_confirm = tkinter.Button(search_top, text="Confirm", command=select_where).place(x=50, y=160)
        btn_back = tkinter.Button(search_top, text='Back', command=search_top.withdraw).place(x=170, y=160)

    def update_ware():
        """更改仓库物品信息"""

        re_costs, re_clerk = '', ''

        change_top = tkinter.Toplevel()
        change_top.title('更改仓储货物信息')
        change_top.geometry('280x240+600+400')
        change_top.resizable(0, 0)

        # 提示用户ID的label
        tkinter.Label(change_top, text='物品存储编号: ').place(x=20, y=10)
        var_id = tkinter.StringVar()
        var_id.set('请输入物品id')
        tkinter.Entry(change_top, textvariable=var_id, width=15).place(x=100, y=10)

        label1 = tkinter.Label(change_top, text='成本：').place(x=30, y=60)
        label2 = tkinter.Label(change_top, text='仓库负责人：').place(x=30, y=90)
        label3 = tkinter.Label(change_top, text='采购单号：').place(x=30, y=120)
        label4 = tkinter.Label(change_top, text='入库时间：').place(x=30, y=150)

        var_costs = tkinter.StringVar()  # 定义变量
        var_costs.set(re_costs)
        var_clerk = tkinter.StringVar()
        var_clerk.set(re_clerk)

        entry1 = tkinter.Entry(change_top, textvariable=var_costs).place(x=110, y=60)
        entry2 = tkinter.Entry(change_top, textvariable=var_clerk).place(x=110, y=90)

        # 不能更改的订单项和日期项
        var_ware_pur = tkinter.StringVar()
        var_ware_pur.set('')
        var_ware_date = tkinter.StringVar()
        var_ware_date.set('')
        label_pur = tkinter.Label(change_top, textvariable=var_ware_pur).place(x=110, y=120)
        label_date = tkinter.Label(change_top, textvariable=var_ware_date).place(x=110, y=150)

        def check_uid():
            try:
                link.conn()
                re_costs = link.select_para(sql_ware4, (var_id.get(),))
                re_clerk = link.select_para(sql_ware5, (var_id.get(),))
                re_pur = link.select_para(sql_ware2, (var_id.get(),))
                re_date = link.select_para(sql_ware3, (var_id.get(),))

                var_costs.set(str(re_costs)[3:-4])
                var_clerk.set(str(re_clerk)[3:-4])

                var_ware_pur.set(re_pur)
                var_ware_date.set(re_date)

                link.close_conn()
            except:
                info = sys.exc_info()
                info1 = list(info)
                all_info = str(info1[1])
                messagebox.showerror(title='Error', message=all_info)

        def change_info():
            try:
                para = {
                    'stock_id': str(var_id.get()).strip(),
                    'costs_': str(var_costs.get()).strip(),
                    'ware_clerk': str(var_clerk.get()).strip()
                }
                link.conn()
                result = link.insert_update_para(sql_update_ware, para)
                if result:
                    messagebox.showinfo(title='提示', message='更改成功')
                link.close_conn()
            except:
                info = sys.exc_info()
                info1 = list(info)
                all_info = str(info1[1])
                messagebox.showerror(title='Error', message=all_info)

        btn_uid = tkinter.Button(change_top, text='Checked', font=('Consolas', 8), command=check_uid).place(x=220, y=10)
        btn_confirm = tkinter.Button(change_top, text="Confirm", command=change_info).place(x=50, y=190)
        btn_back = tkinter.Button(change_top, text='Back', command=change_top.withdraw).place(x=170, y=190)


    # 客户订单的方法们
    def select_cus_ord():
        """查询所有客户订单"""
        try:
            mylist.delete(0, 'end')  # 清空list
            link.conn()
            results = link.select(sql_select_cus_ord)
            for result in results:
                into_mylist(result)
            into_head_label(link.get_head())
            var_count.set(str(link.get_row()) + ' rows')  # 得到结果行数
            link.close_conn()
        except:
            info = sys.exc_info()
            info1 = list(info)
            all_info = str(info1[1])
            messagebox.showerror(title='Error', message=all_info)

    def search_order():
        """查询订单"""
        search_top = tkinter.Toplevel()
        search_top.geometry('280x280+600+400')
        search_top.resizable(0, 0)

        label1 = tkinter.Label(search_top, text='订单id：').place(x=30, y=10)
        label2 = tkinter.Label(search_top, text='归还时间：').place(x=30, y=40)
        label3 = tkinter.Label(search_top, text='租价：').place(x=30, y=70)
        label4 = tkinter.Label(search_top, text='用户id：').place(x=30, y=100)
        label5 = tkinter.Label(search_top, text='存储id：').place(x=30, y=130)
        label6 = tkinter.Label(search_top, text='送货人：').place(x=30, y=160)

        var_ordid = tkinter.StringVar()
        var_ordid.set('')
        var_date = tkinter.StringVar()
        var_date.set('')
        var_price = tkinter.DoubleVar()
        var_price.set(0.0)
        var_uid = tkinter.IntVar()
        var_stid = tkinter.StringVar()
        var_stid.set('')
        var_de = tkinter.StringVar()
        var_de.set('')

        entry1 = tkinter.Entry(search_top, textvariable=var_ordid).place(x=100, y=10)
        entry1 = tkinter.Entry(search_top, textvariable=var_date).place(x=100, y=40)
        entry1 = tkinter.Entry(search_top, textvariable=var_price).place(x=100, y=70)
        entry1 = tkinter.Entry(search_top, textvariable=var_uid).place(x=100, y=100)
        entry1 = tkinter.Entry(search_top, textvariable=var_stid).place(x=100, y=130)
        entry1 = tkinter.Entry(search_top, textvariable=var_de).place(x=100, y=160)

        ck_num1 = tkinter.IntVar()
        ck_num2 = tkinter.IntVar()

        ck1 = tkinter.Checkbutton(search_top, text='已还', variable=ck_num1, onvalue=1, offvalue=0).place(x=60, y=190)
        ck2 = tkinter.Checkbutton(search_top, text='未还', variable=ck_num2, onvalue=1, offvalue=0).place(x=160, y=190)

        btn_confirm = tkinter.Button(search_top, text="Confirm", command=None).place(x=50, y=240)
        btn_back = tkinter.Button(search_top, text='Back', command=search_top.withdraw).place(x=170, y=240)
#-----------------

    def return_stock():
        """订单返回仓库"""
        return_top = tkinter.Toplevel()
        return_top.geometry('280x280+600+400')
        return_top.resizable(0, 0)
        tkinter.Label(return_top, text='输入返还订单号: ').place(x=20, y=10)

        var_id = tkinter.StringVar()
        var_id.set('输入订单号')
        tkinter.Entry(return_top, textvariable=var_id, width=15).place(x=120, y=10)

        label1 = tkinter.Label(return_top, text='归还时间：').place(x=30, y=60)
        label2 = tkinter.Label(return_top, text='租价：').place(x=30, y=90)
        label3 = tkinter.Label(return_top, text='送货人：').place(x=30, y=120)
        label4 = tkinter.Label(return_top, text='用户id：').place(x=30, y=150)
        label5 = tkinter.Label(return_top, text='存储id：').place(x=30, y=180)
        label6 = tkinter.Label(return_top, text='归还状态：').place(x=30, y=210)

        var_date = tkinter.StringVar()
        var_date.set('当前时间')
        var_price = tkinter.DoubleVar()
        var_de = tkinter.StringVar()

        entry1 = tkinter.Entry(return_top, textvariable=var_date).place(x=100, y=60)
        entry2 = tkinter.Entry(return_top, textvariable=var_price).place(x=100, y=90)
        entry3 = tkinter.Entry(return_top, textvariable=var_de).place(x=100, y=120)


        var_uid = tkinter.StringVar()
        var_stid = tkinter.StringVar()
        var_status = tkinter.StringVar()

        label_uid = tkinter.Label(return_top, textvariable=var_uid).place(x=100, y=150)
        label_stid = tkinter.Label(return_top, textvariable=var_stid).place(x=100, y=180)
        label_status = tkinter.Label(return_top, textvariable=var_status).place(x=100, y=210)

        def check_id():
            pass

        def return_st():
            pass

        btn_id = tkinter.Button(return_top, text='Checked', font=('Consolas', 8), command=check_id).place(x=230, y=10)
        btn_confirm = tkinter.Button(return_top, text="Confirm", command=return_st).place(x=50, y=240)
        btn_back = tkinter.Button(return_top, text='Back', command=return_top.withdraw).place(x=170, y=240)


    # 用户信息的方法们
    def select_cus():
        """查询所有用户信息"""
        try:
            mylist.delete(0, 'end')  # 清空list
            link.conn()
            results = link.select(sql_select_cus)
            for result in results:
                into_mylist(result)
            into_head_label(link.get_head())
            var_count.set(str(link.get_row()) + ' rows')  # 得到结果行数
            link.close_conn()
        except:
            info = sys.exc_info()
            info1 = list(info)
            all_info = str(info1[1])
            messagebox.showerror(title='Error', message=all_info)

    def search_cus():
        """筛选用户"""
        search_top = tkinter.Toplevel()
        search_top.title('查询用户信息')
        search_top.geometry('280x180+600+400')
        search_top.resizable(0, 0)
        search_top.wm_attributes("-topmost", 1)

        label1 = tkinter.Label(search_top, text='用户ID号：').place(x=20, y=10)
        label2 = tkinter.Label(search_top, text='用户名字：').place(x=20, y=40)
        label3 = tkinter.Label(search_top, text='性别：').place(x=20, y=70)
        label4 = tkinter.Label(search_top, text='VIP？：').place(x=20, y=100)

        var_user_id = tkinter.StringVar()  # 定义变量
        var_user_id.set('')
        var_user_name = tkinter.StringVar()
        var_user_name.set('')
        var_gender = tkinter.StringVar()
        var_gender.set('')
        var_vip = tkinter.StringVar()
        var_vip.set('')

        entry1 = tkinter.Entry(search_top, textvariable=var_user_id).place(x=110, y=10)
        entry2 = tkinter.Entry(search_top, textvariable=var_user_name).place(x=110, y=40)
        entry3 = tkinter.Entry(search_top, textvariable=var_gender).place(x=110, y=70)
        entry4 = tkinter.Entry(search_top, textvariable=var_vip).place(x=110, y=100)

        def select_where():
            try:
                mylist.delete(0, 'end')
                link.conn()
                para = {
                    'user_id': '%' + str(var_user_id.get()) + '%',
                    'user_name': '%' + str(var_user_name.get()) + '%',
                    'gender': '%' + str(var_gender.get()) + '%',
                    'vip': '%' + str(var_vip.get()) + '%'
                }
                results = link.select_para(sql_search_cus, para)
                for result in results:
                    into_mylist(result)
                into_head_label(link.get_head())  # 改变表头
                var_count.set(str(link.get_row()) + ' rows')  # 得到结果行数
                link.close_conn()
            except:
                info = sys.exc_info()
                info1 = list(info)
                all_info = str(info1[1])
                messagebox.showerror(title='Error', message=all_info)

        btn_confirm = tkinter.Button(search_top, text="Confirm", command=select_where).place(x=50, y=130)
        btn_back = tkinter.Button(search_top, text='Back', command=search_top.withdraw).place(x=170, y=130)

    def update_cus():
        """更改用户"""
        re_name, re_gender, re_vip, re_pwd, re_address = '', '', '', '', ''

        change_top = tkinter.Toplevel()
        change_top.title('更改用户信息')
        change_top.geometry('280x260+600+400')
        change_top.resizable(0, 0)
        change_top.wm_attributes("-topmost", 1)

        # 提示用户ID的label
        tkinter.Label(change_top, text='输入用户id: ').place(x=20, y=10)
        var_uid = tkinter.StringVar()
        var_uid.set('请输入用户id')
        tkinter.Entry(change_top, textvariable=var_uid, width=15).place(x=100, y=10)

        label1 = tkinter.Label(change_top, text='用户名：').place(x=30, y=60)
        label2 = tkinter.Label(change_top, text='性别：').place(x=30, y=90)
        label3 = tkinter.Label(change_top, text='VIP？：').place(x=30, y=120)
        label4 = tkinter.Label(change_top, text='密码：').place(x=30, y=150)
        label5 = tkinter.Label(change_top, text='联系地址：').place(x=30, y=180)

        var_name = tkinter.StringVar()  # 定义变量
        var_name.set(re_name)
        var_gender = tkinter.StringVar()
        var_gender.set(re_gender)
        var_vip = tkinter.StringVar()
        var_vip.set(re_vip)
        var_passwd = tkinter.StringVar()
        var_passwd.set(re_pwd)
        var_address = tkinter.StringVar()
        var_address.set(re_address)

        entry1 = tkinter.Entry(change_top, textvariable=var_name).place(x=100, y=60)
        entry2 = tkinter.Entry(change_top, textvariable=var_gender).place(x=100, y=90)
        entry3 = tkinter.Entry(change_top, textvariable=var_vip).place(x=100, y=120)
        entry4 = tkinter.Entry(change_top, textvariable=var_passwd).place(x=100, y=150)
        entry5 = tkinter.Entry(change_top, textvariable=var_address).place(x=100, y=180)

        def check_uid():
            try:
                link.conn()
                re_name = link.select_para(sql_cus2, (var_uid.get(),))
                re_gender = link.select_para(sql_cus3, (var_uid.get(),))
                re_vip = link.select_para(sql_cus4, (var_uid.get(),))
                re_pwd = link.select_para(sql_cus5, (var_uid.get(),))
                re_address = link.select_para(sql_cus6, (var_uid.get(),))

                var_name.set(str(re_name)[3:-4])
                var_gender.set(str(re_gender)[3:-4])
                var_vip.set(str(re_vip)[3:-4])
                var_passwd.set(str(re_pwd)[3:-4])
                var_address.set(str(re_address)[3:-4])
            except:
                info = sys.exc_info()
                info1 = list(info)
                all_info = str(info1[1])
                messagebox.showerror(title='Error', message=all_info)

            link.close_conn()

        def change_info():
            try:
                para = {
                    'user_id': str(var_uid.get()).strip(),
                    'user_name': str(var_name.get()).strip(),
                    'sex_': str(var_gender.get()).strip(),
                    'vip_': str(var_vip.get()).strip(),
                    'user_pwd': str(var_passwd.get()).strip(),
                    'user_address': str(var_address.get()).strip()
                }
                link.conn()
                result = link.insert_update_para(sql_update_cus, para)
                if result:
                    messagebox.showinfo(title='提示', message='更改成功')
                link.close_conn()
            except:
                info = sys.exc_info()
                info1 = list(info)
                all_info = str(info1[1])
                messagebox.showerror(title='Error', message=all_info)

        btn_uid = tkinter.Button(change_top, text='Checked', font=('Consolas', 8), command=check_uid).place(x=220, y=10)
        btn_confirm = tkinter.Button(change_top, text="Confirm", command=change_info).place(x=50, y=210)
        btn_back = tkinter.Button(change_top, text='Back', command=change_top.withdraw).place(x=170, y=210)

    # 终端启动按钮
    btn_terminal = tkinter.Button(window_main, image=img_terminal, relief=tkinter.FLAT, command=run_terminal).place(x=170, y=0)

    # 采购表的操作按钮
    btn_show_data_pur = tkinter.Button(window_main, image=img_show_data_pur, command=select_pur).place(x=20, y=40)
    btn_pur_insert = tkinter.Button(window_main, text='添加采购订单', command=insert_pur).place(x=90, y=40)
    btn_pur_import = tkinter.Button(window_main, text='采购订单入库', command=insert_pur_ware).place(x=180, y=40)
    btn_pur_update_delete = tkinter.Button(window_main, text='更改采购订单', command=update_pur).place(x=90, y=80)
    btn_pur_select = tkinter.Button(window_main, text='查询采购订单', command=search_pur).place(x=180, y=80)

    # 仓库表的操作按钮
    btn_show_data_ware = tkinter.Button(window_main, image=img_show_data_warehouse, command=select_ware).place(x=20, y=150)
    btn_ware_update_delete = tkinter.Button(window_main, text='更改库存', width=11, command=update_ware).place(x=90, y=150)
    btn_ware_select = tkinter.Button(window_main, text='具体查询', width=11, command=search_ware).place(x=90, y=190)

    #用户订单的操作按钮
    btn_show_data_cus_order = tkinter.Button(window_main, image=img_show_date_customer_order, command=select_cus_ord).place(x=20, y=260)
    btn_return_cus_order = tkinter.Button(window_main, text='订单返库', width=11, command=return_stock).place(x=90, y=260)
    btn_order_select = tkinter.Button(window_main, text='查询订单', width=11, command=search_order).place(x=90, y=300)

    # 用户信息的操作按钮
    btn_show_data_cus = tkinter.Button(window_main, image=img_show_data_customer, command=select_cus).place(x=20, y=400)
    btn_cus_update_delete = tkinter.Button(window_main, text='用户信息修改', command=update_cus).place(x=110, y=440)
    btn_cus_select = tkinter.Button(window_main, text='用户信息查询', command=search_cus).place(x=110, y=400)

    window_main.mainloop()
