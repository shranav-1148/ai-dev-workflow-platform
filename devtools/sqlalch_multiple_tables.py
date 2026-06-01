from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///gfg.db', echo=True)
Base = declarative_base()

# Defining Student and Fee classes where student has a one-to-many with fees
class Student(Base):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    
    fees = relationship("Fee", back_populates="student")
    
class Fee(Base):
    __tablename__ = 'fees'
    
    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
    student_id = Column(Integer, ForeignKey('students.id'))

    student = relationship("Student", back_populates="fees")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Adding a student and their fees to the database
# s1 = Student(name='John Doe', age=20)
# s1.fees = [
#     Fee(amount=100),
#     Fee(amount=200)
# ]

# session.add(s1)
# session.commit()

# student_fees = session.query(Student).filter_by(name='John Doe').one().fees

# for fee in student_fees:
#     print(fee.amount)


# Joining the Student and Fee tables to retrieve student names and their fees
students = [
    Student(name='John Doe', age=20),
    Student(name='Jane Smith', age=22),
    Student(name='Bob Brown', age=25),
    Student(name='Alice Jones', age=23)
]

fees = [
    Fee(amount=5000),
    Fee(amount=6000),
    Fee(amount=4500),
    Fee(amount=5500)
]

for i in range(len(students)):
    students[i].fees.append(fees[i])
    session.add(students[i])

session.commit()

from sqlalchemy.orm import joinedload

# Query all students and their fees using joinedload
# This will load the fees for each student in a single query, avoiding the N+1 problem
students = session.query(Student).options(joinedload(Student.fees)).all()

for student in students:
    print(f'{student.name} ({student.age}):')
    for fee in student.fees:
        print(f'- {fee.amount}')

# Query students and fees using a join
# This will return a list of tuples where each tuple contains a student and their fee
from sqlalchemy.orm import aliased

student = aliased(Student)
fee = aliased(Fee)
stmt = session.query(student, fee)\
              .join(fee, student.id == fee.student_id)\
              .order_by(student.name)\
              .all()

for s, f in stmt:
    print(f'{s.name} ({s.age}): {f.amount}')


    from sqlalchemy import delete


# Multi-table delete procedure
# delete(tablename_1).where(tablename_1.c.column_name== tablename_2.c.column_name)
# .where(tablename_2.c.column_name== 'value')