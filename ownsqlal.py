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


customer = Table('customer', metadata,
Column('customer_id', Integer(), primary_key=True),
Column('customer_name', String(140), index=True),
Column('location_id', ForeignKey('location.location_id'))

)



location = Table('location', metadata,
Column('location_id', Integer(), primary_key=True),
Column('location_residence', String(140), index=True),
)

def custins(name):
	ins=customer.insert().values(
        customer_name=name
		)
	print(str(ins))
	out=ins.compile().params
	print(out)
	result = connection.execute(ins)

def locationins(residence):
	ins=location.insert().values(
        location_residence=residence
		)
	print(str(ins))
	out=ins.compile().params
	print(out)
	result = connection.execute(ins)

def queryall(table):
    s = select([table])
    s = s.limit(2)
    rp = connection.execute(s)
    for i in rp:
    	print(i)

def queryselection(list, list1):
   s = select([list, list1])
   rp = connection.execute(s)
   print(rp.keys())
   for i in rp:
       print(i)




queryall(customer)
metadata.create_all(engine)