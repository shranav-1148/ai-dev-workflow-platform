from sqlalchemy import create_engine

user = 'root'
password = 'password'
host = "127.0.0.1"
port = 3306
database = "test_db"



# mysql connection
# using the mysql dialect and pymysql driver
def get_sql_connection():
    engine = create_engine (
        f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    )

    return engine

# using the postgre dialect
def get_postgresql_connection():
    engine = create_engine(
        f"postgresql://{user}:{password}@{host}:{port}/{database}"
    )
    return engine

if __name__ == "__main__":
    try:
        engine = get_sql_connection()
        print(f"Connection to the {host} for user {user} was successfully.")
    except Exception as e:
        print("Conneection could not be made due to the following error:\n", e)