# -*- coding: utf-8 -*-
# producer: 王健吉(leimilia)

def get_config():
    with open('config.ini', 'r', encoding='utf-8-sig') as obj:
        info = obj.readlines()

    str_info = str(info[0])
    dict_info = eval(str_info)
    return dict_info


class Trans():
    def __init__(self):
        dict_info = get_config()
        self.user_name = dict_info['config']['username']
        self.user_pwd = dict_info['config']['passpwd']
        self.host = dict_info['config']['host']
        self.port = dict_info['config']['port']
        self.sid = dict_info['config']['sid']
        self.database_address = None

        self.ver = None
        self.row_count = 5

    def reset_all_trans(self):
        self.user_name = None
        self.user_pwd = None
        self.host = None
        self.port = None
        self.sid = None
        self.database_address = None

    def get_database_address(self):
        self.database_address = str(self.host) + ':' + str(self.port) + '/' + str(self.sid)
        return self.database_address