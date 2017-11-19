# coding: utf-8

import sys
import cx_Oracle

def terminal(trans):
    connection = cx_Oracle.connect(trans.user_name, trans.user_pwd, trans.database_address)
    cursor = connection.cursor()

    cursor.execute("select * from v$version")
    versions = cursor.fetchall()
    for version in versions:
        print('%s' % version)

    try:
        while True:
            sql = input('Enter the SQL command(q to quit): ')
            if sql == 'Q' or sql == 'q':
                cursor.close()
                connection.close()
                print('End the link.')
                break
            else:
                cursor.execute(sql)
                all_data = cursor.fetchall()

                for data in all_data:
                    print(data)

    except:
        info = sys.exc_info()
        print(info)

        while True:
            sql = input('Enter the SQL command(q to quit): ')
            if sql == 'Q' or sql == 'q':
                cursor.close()
                connection.close()
                print('End the link.')
                break
            else:
                cursor.execute(sql)
                all_data = cursor.fetchall()

                for data in all_data:
                    print(data)



