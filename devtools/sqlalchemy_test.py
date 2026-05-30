import sqlalchemy as db

# Making Database connection
# dialect : mysql, postgresql, sqlite, oracle, mssql
# driver: pymysql, psycopg2, sqlite, cx_oracle, pyodbc
# username/password: login credentials
# host/port: databse server address and port
# database : database name
engine = db.create_engine('dialect+driver://user:pass@host:port/db')


# SELECT * FROM films WHERE certification = 'PG'
db.select([films]).where(films.columns.certification == 'PG')


# SELECT * FROM files WHERE certification = 'R' and release_year > 2003
db.select([files]).where(db.and_(files.columns.certification == 'R',
                                  files.columns.release_year > 2003))
