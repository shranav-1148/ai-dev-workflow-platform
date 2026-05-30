import sqlalchemy as db

engine = db.create_engine('sqlite:///users.db', echo = True)


metadata_obj = db.MetaData()

profile = db.Table(
    'profile',
    metadata_obj,
    db.Column('email', db.String, primary_key = True),
    db.Column('name', db.String),
    db.Column('contact', db.Integer),
)

metadata_obj.create_all(engine)