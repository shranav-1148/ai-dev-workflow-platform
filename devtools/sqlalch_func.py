from sqlalchemy import and_, case, create_engine, MetaData, literal,select,func


engine = create_engine("mysql+pymysql://userName:password@host:port/dbName")
metadata = MetaData()
metadata.reflect(bind=engine)

studentTable=metadata.tables['student']

# Using func to calculate the average score
query=select(func.avg(studentTable.c.score).label("Average"))
with engine.connect() as connect:
    result=connect.execute(query).fetchall()
    print("Average of Student's score is::",result[0][0])

# using func to calculate the total count of students
query=select(func.count(studentTable.c.name).label("Count of Students"))
with engine.connect() as connect:
    result=connect.execute(query).fetchall()
    print("Total count of students in class::",result[0][0])

# using func to calculate the sum of scores of students
query=select(func.sum(studentTable.c.score).label("Sum of scores"))
with engine.connect() as connect:
    result=connect.execute(query).fetchall()
    print("Sum of scores of students::",result[0][0])

#  Find the maximum score
query=select(func.max(studentTable.c.score).label("Max Score"))
with engine.connect() as connect:
    result=connect.execute(query).fetchall()
    print("Maximum Score in Student scores::",result[0][0])

# Grouping the students by grade and finding the max score in each grade
query=select(studentTable.c.grade, func.max(studentTable.c.score).
             label("maxscore")).group_by(studentTable.c.grade)
with engine.connect() as connect:
    result=connect.execute(query).fetchall()
    print("grade || max score")
    for data in result:
      print(data[0],"||",data[1])

    query=select(studentTable.c.grade,func.min(studentTable.c.score),func.count(studentTable.c.score))
with engine.connect() as connect:
    result=connect.execute(query).fetchall()
    print("grade | min value | count")
    for data in result:
      print(data[0],data[1],data[2])    

#  Minimum value in column
query=select(studentTable.c.grade,func.min(studentTable.c.score),func.count(studentTable.c.score))
with engine.connect() as connect:
    result=connect.execute(query).fetchall()
    print("grade | min value | count")
    for data in result:
      print(data[0],data[1],data[2])


# Calculate the floor value of a number
query=select(func.floor(3.6))

with engine.connect() as connect:
    result=connect.execute(query).fetchall()
    print("Floor value of 3.6 is",result[0][0])

# Calculate the ceiling value of a number
    query=select(func.abs(10),literal(10),func.abs(-20),literal(-20),func.abs(30+43-100),literal(30+43-100))
with engine.connect() as connect:
    result=connect.execute(query).fetchall()
print("Abs values of abs value and actual value::",*result[0])

# Calculate length of string
query=select(studentTable.c.name,func.length(studentTable.c.name).label("Sum of scores"))
with engine.connect() as connect:
    result=connect.execute(query).fetchall()
    for data in result:
        print(data[0],data[1])

# Convert string to lower case
query=select(func.lower(studentTable.c.name).label("Upper"))
with engine.connect() as connect:
    result=connect.execute(query).fetchall()
    for data in result:
        print(data[0])

# convert string to upper case
query=select(func.upper(studentTable.c.name).label("Upper"))
with engine.connect() as connect:
    result=connect.execute(query).fetchall()
    for data in result:
        print(data[0])

# Calculate the current data and time
query=select(func.now().label("now"))
with engine.connect() as connect:
    result=connect.execute(query).fetchall()
    for data in result:
        print(data[0])


# Calculate the current date and time separately
query=select(func.current_date().label("date"),func.current_time().label("time"))
with engine.connect() as connect:
    result=connect.execute(query).fetchall()
    for data in result:
        print(data[0],data[1])

# Concat multiple strings into one string by grouping them together
query = select(
    studentTable.c.grade,
    func.group_concat(studentTable.c.name, ',').label('names')
).group_by(studentTable.c.grade)
with engine.connect() as connect:
    result=connect.execute(query).fetchall()
    for data in result:
        print(data[0],data[1])


# Using case statement to assign grade points based on score
query = select(
    studentTable.c.name,studentTable.c.score,
    case(
            (and_(studentTable.c.score>=91,studentTable.c.score<=100),10),
            (and_(studentTable.c.score>=81, studentTable.c.score<=90) , 9),
            (and_(studentTable.c.score>=71, studentTable.c.score<=80) , 8),
            (and_(studentTable.c.score>=61, studentTable.c.score<=70) , 7),
            (and_(studentTable.c.score>=51, studentTable.c.score<=60) , 6),
            (and_(studentTable.c.score>=41, studentTable.c.score<=50) , 5),
            else_=0
    ).label("Grade Points")
)

with engine.connect() as connect:
    result=connect.execute(query).fetchall()
    for data in result:
        print(*data)