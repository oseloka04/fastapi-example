import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import Settings

#SQLALCHEMY_DATABASE_URL ='postgresql://{Settings.database_username}:{Settings.database_password}@{Settings.database_hostname}:{Settings.database_port}/{Settings.database_name}'
SQLALCHEMY_DATABASE_URL ='postgresql://postgres:surgeon@localhost:5432/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
        
    finally:
        db.close() 


#while True:

 #try:
    # conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
    # password='surgeon', cursor_factory=RealDictCursor)
    # cursor = conn.cursor()
     #print('Database was connected succesfully')
     #break
 #except Exception as error:
    #print('connecting to database failed') 
    #print('error', error)
    #time.sleep(2)   
