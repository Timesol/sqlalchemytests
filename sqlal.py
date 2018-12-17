from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, Numeric, String, ForeignKey, Boolean
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy import PrimaryKeyConstraint, UniqueConstraint, CheckConstraint
from sqlalchemy import Index
from sqlalchemy.sql import select
from sqlalchemy import desc
from sqlalchemy.sql import func
from sqlalchemy import cast
from sqlalchemy import update
from sqlalchemy import insert

metadata=MetaData()
engine=create_engine('mysql+pymysql://sqltest:Katze7436!@localhost:3306/sqltest')
connection=engine.connect()


cookies = Table('cookies', metadata,
Column('cookie_id', Integer(), primary_key=True),
Column('cookie_name', String(50), index=True),
Column('cookie_recipe_url', String(255)),
Column('cookie_sku', String(55)),
Column('quantity', Integer()),
Column('unit_cost', Numeric(12, 2))
)


users = Table('users', metadata,
Column('user_id', Integer(), primary_key=True),
Column('username', String(15), nullable=False, unique=True),
Column('email_address', String(255), nullable=False),
Column('phone', String(20), nullable=False),
Column('password', String(25), nullable=False),
Column('created_on', DateTime(), default=datetime.now),
Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now)
)

orders = Table('orders', metadata,
Column('order_id', Integer(), primary_key=True),
Column('user_id', ForeignKey('users.user_id')),
Column('shipped', Boolean(), default=False)
)


line_items = Table('line_items', metadata,
Column('line_items_id', Integer(), primary_key=True),
Column('order_id', ForeignKey('orders.order_id')),
Column('cookie_id', ForeignKey('cookies.cookie_id')),
Column('quantity', Integer()),
Column('extended_cost', Numeric(12, 2))
)


CheckConstraint('unit_cost >= 0.00', name='unit_cost_positive')
Index('ix_cookies_cookie_name', 'cookie_name')

metadata.create_all(engine)




columns = [orders.c.order_id, users.c.username, users.c.phone,
cookies.c.cookie_name, line_items.c.quantity,
line_items.c.extended_cost]
cookiemon_orders = select(columns)
cookiemon_orders = cookiemon_orders.select_from(orders.join(users).join(
line_items).join(cookies)).where(users.c.username ==
'cookiemon')
result = connection.execute(cookiemon_orders).fetchall()
for row in result:
    print(row)


columns = [users.c.username, func.count(orders.c.order_id)]
all_orders = select(columns)
all_orders = all_orders.select_from(users.outerjoin(orders))
all_orders = all_orders.group_by(users.c.username)
result = connection.execute(all_orders).fetchall()
for row in result:
    print(row)

