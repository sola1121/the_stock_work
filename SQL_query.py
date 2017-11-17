# coding: utf-8
# producer: 王健吉(leimilia)

# 用于采购订单
sql_select_pur = 'select * from purchases'

sql_pur_ware1 = 'insert into stocks(stock_id, purchase_id, entry_date, costs, warehouse_clerk, quantity) ' \
               'values (:stock_id, :pur_id, :en_date ,:costs, :clerk, :quantity)'
sql_pur_ware2 = 'insert into stocks(stock_id, purchase_id, entry_date, costs, warehouse_clerk, quantity) ' \
               'values (:stock_id, :pur_id, sysdate ,:costs, :clerk, :quantity )'

sql_insert_pur1 = 'insert into purchases values(:pur_id, :pur_date, :price, :agent, :category, :brand, :quantity)'
sql_insert_pur2 = 'insert into purchases values(:pur_id, sysdate, :price, :agent, :category, :brand, :quantity)'
sql_pur_status = 'update purchases set status = 1 where purchase_id =:1'

sql_pur1 = 'select purchase_id from purchases where purchase_id =:1'
sql_pur2 = 'select purchase_date from purchases where purchase_id =:1'
sql_pur3 = 'select purchase_price from purchases where purchase_id =:1'
sql_pur4 = 'select purchasing_agent from purchases where purchase_id =:1'
sql_pur5 = 'select clothing_category from purchases where purchase_id =:1'
sql_pur6 = 'select clothing_brand from purchases where purchase_id =:1'
sql_pur7 = 'select quantity from purchases where purchase_id =:1'
sql_pur8 = 'select status from purchases where purchase_id =:1'
sql_update_pur = 'update purchases set purchase_date =:pur_date, purchase_price =:pur_price, ' \
                 'purchasing_agent =:pur_agent, clothing_ =:pur_category, clothing_brand =:pur_brand, ' \
                 'quantity =:pur_quantity where purchase_id =:pur_id'


sql_search_pur = "select * from purchases " \
                 "where purchase_date like :time " \
                 "and purchasing_agent like :duty " \
                 "and clothing_brand like :brand " \
                 "and status like :status "

# 用于仓库
sql_select_ware = 'select * from stocks'

sql_ware1 = 'select stock_id from stocks where stock_id =:1'
sql_ware2 = 'select purchase_id from stocks where stock_id =:1'
sql_ware3 = 'select entry_date from stocks where stock_id =:1'
sql_ware4 = 'select costs from stocks where stock_id =:1'
sql_ware5 = 'select warehouse_clerk from stocks where stock_id =:1'
sql_update_ware = "update stocks set costs =:costs_, warehouse_clerk =:ware_clerk where stock_id=:stock_id "

sql_search_ware = "select * from stocks " \
                  "where stock_id like :stock " \
                  "and purchase_id like :purchase " \
                  "and entry_date like :en_date " \
                  "and costs like :costs " \
                  "and warehouse_clerk like :clerk "


# 用于用户订单
sql_select_cus_ord = 'select * from rents'

sql_ord1 = 'select rent_id from rents where rent_id =:rent_id '
sql_ord2 = 'select rent_date from rents where rent_date =:rent_date '
sql_ord3 = 'select rent_price from rents where rent_id =:rent_id'
sql_ord4 = 'select user_id from rents where rent_id =:rent_id'
sql_ord5 = 'select stock_id from rents where rent_id =:rent_id'
sql_ord6 = 'select deliveryman from rents where rent_id =:rent_id'
sql_ord7 = 'select status from rents where status =:rent_id '

sql_ord_stock1 = "update rents set status='已还' where rent_id =:rent_id "
sql_ord_stock2 = "update stocks set quantity=quantity+1 where stock_id =:stock_id "


sql_update_cus_ord_stock = 'update '

# 用于用户信息
sql_select_cus = 'select * from users'

sql_search_cus = "select * from users " \
                "where user_id like :user_id " \
                "and user_name like :user_name " \
                "and gender like :gender " \
                "and vip like :vip "

sql_cus1 = 'select user_id from users where user_id = :1'
sql_cus2 = 'select user_name from users where user_id =:1'
sql_cus3 = 'select gender from users where user_id =:1'
sql_cus4 = 'select vip from users where user_id =:1'
sql_cus5 = 'select passwd from users where user_id =:1'
sql_cus6 = 'select address from users where user_id =:1'
sql_update_cus = "update users set user_name=:user_name, gender=:sex_, " \
                 "vip=:vip_, passwd=:user_pwd, address=:user_address where user_id =:user_id"

# 测试sql
sql_test = 'select * from sal_history where salary like :salary'