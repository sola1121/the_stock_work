--采购表 purchases

create table purchases
(purchase_id varchar2(16)
  constraint pur_id_pk primary key,
 purchase_date date default sysdate,
 purchase_price number(8,2) not null,
 purchasing_agent varchar2(16) not null,
 clothing_category varchar2(25) not null,
 clothing_brand varchar2(25) not null,
 quantity number(8,2)
  constraint pur_quan_ck check(quantity > 0));
 
-- 库存表 stocks

create table stocks
(stock_id varchar2(16)
  constraint sto_id_pk primary key,
 purchase_id varchar2(12)
  constraint sto_pur_fk references purchases(purchase_id),
 enter_date date default sysdate,
 costs number(6,2) not null,
 warehouse_clerk varchar2(16) default 'Linda',
 quantity number(8,2)
  constraint sto_quan_ck check(quantity > 0));

-- 用户表 users

create table users
(user_id number(12)
  constraint user_id_pk primary key,
 user_name varchar2(16) not null,
 gender varchar2(4) not null
  constraint user_gen_ck check(gender in('男','女')),
 passwd varchar2(18) not null,
 address varchar2(30),
 balance number(10,2) default 0);


-- 租出表 rents

create table rents
(rent_id varchar2(16)
  constraint rent_id primary key,
 rent_date timestamp default sysdate,
 rent_price number(6,2) not null,
 user_id number(12) not null
  constraint rent_user_fk references users(user_id),
 stock_id varchar2(16) not null
  constraint rent_sto_fk references stocks(stock_id),
 deliveryman varchar2(16) default 'Linda');


-- 归还表 returns

create table returns
(return_id varchar2(16)
  constraint ret_id_pk primary key,
 return_date timestamp default sysdate not null,
 user_id number(12) not null
  constraint ret_user_fk references users(user_id),
 stock_id varchar2(16) not null
  constraint ret_sto_fk references stocks(stock_id),
 warehouse_clerk varchar(15) not null);