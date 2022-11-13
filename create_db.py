from sqlalchemy import create_engine
db_string = 'postgresql+psycopg2://postgres:postgres@localhost:5432'

db = create_engine(db_string, isolation_level='AUTOCOMMIT')


db.execute("CREATE DATABASE AIML;")