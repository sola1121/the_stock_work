# -*- coding: utf-8 -*-
# producer: 王健吉(leimilia)

class Trans():
    def __init__(self):
        self.user_name = None
        self.user_pwd = None
        self.host = 'localhost'
        self.port = '1521'
        self.sid = 'oracle'
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