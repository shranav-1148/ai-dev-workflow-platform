from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, or_, and_, not_

# Create a SQLite engine
engine = create_engine('sqlite:///mydb.database', echo=True)

# Define a metadata object
metadata = MetaData()

# Define a table
students = Table('students', metadata,
                 Column('id', Integer, primary_key=True),
                 Column('name', String),
                 Column('age', Integer),
                 Column('gender', String)
                 )

# Create the table if it does not exist
metadata.create_all(engine)


# Insert some data into the users table
conn = engine.connect()
conn.execute(students.insert(), [
    {'name': 'Alice', 'age': 25, 'gender': 'Female'},
    {'name': 'John', 'age': 30, 'gender': 'Male'},
    {'name': 'Charlie', 'age': 35, 'gender': 'Male'},
    {'name': 'Jane', 'age': 40, 'gender': 'Male'}
])

# Query the database using conjunctions
# Either name is John or Jane
query = students.select().where(
    or_(students.c.name == 'John', students.c.name == 'Jane'))

result = conn.execute(query)

# Print the results
for row in result:
    print(row)

# Query the database using advanced conjunctions
# Either age is greater than or equal to 30 or name is alice and gender is not male
query = students.select().where(
    and_(
        or_(
            students.c.age >= 30,
            students.c.name == 'Alice'
        ),
        not_(students.c.gender == 'Male')
    )
)

result = conn.execute(query)

# Print the results
for row in result:
    print(row)