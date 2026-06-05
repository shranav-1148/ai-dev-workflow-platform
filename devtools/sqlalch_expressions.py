# import necessary packages
from sqlalchemy.engine import result
from sqlalchemy import create_engine, MetaData,\
Table, Column, Numeric, Integer, VARCHAR
from sqlalchemy import text

# establish connections
engine = create_engine(
    "dialect+driver://username:password@host:port/database_name")

# initialize the Metadata Object
meta = MetaData(bind=engine)
MetaData.reflect(meta)

# create a table schema
books = Table(
    'books', meta,
    Column('book_id', Integer, primary_key=True),
    Column('book_price', Numeric),
    Column('genre', VARCHAR),
    Column('book_name', VARCHAR)
)

meta.create_all(engine)

# insert records into the table
statement1 = books.insert().values(book_id=1, 
                                   book_price=12.2,
                                   genre='fiction',
                                   book_name='Old age')
statement2 = books.insert().values(book_id=2, 
                                   book_price=13.2,
                                   genre='non-fiction',
                                   book_name='Saturn rings')

statement3 = books.insert().values(book_id=3,
                                   book_price=121.6,
                                   genre='fiction',
                                   book_name='Supernova')

statement4 = books.insert().values(book_id=4,
                                   book_price=100,
                                   genre='non-fiction',
                                   book_name='History of the world')

statement5 = books.insert().values(book_id=5, 
                                   book_price=1112.2,
                                   genre='fiction', 
                                   book_name='Sun city')

# execute the insert records statement
engine.execute(statement1)
engine.execute(statement2)
engine.execute(statement3)
engine.execute(statement4)
engine.execute(statement5)


# EXECUTING SELECT STATEMENT USING TEXT()
# write the SQL query inside the text() block
sql = text('SELECT * from BOOKS WHERE BOOKS.book_price > 100')
results = engine.execute(sql)

# Fetch all the records
result = engine.execute(sql).fetchall()
  
# View the records
for record in result:
    print("\n", record)



# EXECUTING INSERT STATEMENT USING TEXT() BLOCK
# define a tuple of dictionary of values to be inserted
data = ( { "book_id": 6, "book_price": 400, 
          "genre": "fiction",
          "book_name": "yoga is science" },
         { "book_id": 7, "book_price": 800, 
          "genre": "non-fiction",
          "book_name": "alchemy tutorials" },
)

# write the insert statement
statement = text("""INSERT INTO BOOKS\
(book_id, book_price, genre, book_name) \
VALUES(:book_id, :book_price, :genre, :book_name)""")

# insert the data one after other using
# execute statement by unpacking dictionary  elements
for line in data:
    engine.execute(statement, **line)

# write the SQL query to check
# whether the records are inserted
sql = text("SELECT * FROM BOOKS ")

results = engine.execute(sql)

# View the records
for record in results:
    print("\n", record)



# EXECUTING UPDATE STATEMENT
# Get the `books` table from the Metadata object
BOOKS = meta.tables['books']

# update
stmt = BOOKS.update().where(BOOKS.c.genre == 'non-fiction'
                           ).values(genre='sci-fi')
engine.execute(stmt)

# write the SQL query inside the
# text() block to fetch all records
sql = text("SELECT * from BOOKS")

# Fetch all the records
result = engine.execute(sql).fetchall()

# View the records
for record in result:
    print("\n", record)

# EXECUTING DELETE STATEMENT
# Get the `books` table from the Metadata object
BOOKS = meta.tables['books']

# delete
dele = BOOKS.delete().where(BOOKS.c.genre == "fiction")

engine.execute(dele)

# write the SQL query inside the
# text() block to fetch all records
sql = text("SELECT * from BOOKS")

# Fetch all the records
result = engine.execute(sql).fetchall()

# View the records
for record in result:
    print("\n", record)