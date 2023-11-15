import mysql.connector as mysql
from mysql.connector import Error

def createdatabase(user:str,passw:str):
    db = mysql.connect(
        host="localhost", 
        user=user, 
        passwd=passw)
    curs = db.cursor()
    curs.execute("CREATE DATABASE Jobs")

def creattables(user:str,passw:str):
    db = mysql.connect(
        host="localhost", 
        user=user, 
        passwd=passw, 
        database="Jobs")
    
    curs = db.cursor()

    location = "CREATE TABLE Location(" \
                    "longitude FLOAT(6,4) NOT NULL" \
                    "latitude FLOAT(6,4) NOT NULL" \
                    "location VARCHAR(100) NOT NULL," \
                    "country VARCHAR(100) NOT NULL" \
                    "PRIMARY KEY (longitude, latitude)" \
                    ");"
    
    role = "CREATE TABLE Role("\
                    "responsibilities VARCHAR(250) NOT NULL" \
                    "skills VARCHAR(300) NOT NULL" \
                    "job_description VARCHAR(430) NOT NULL" \
                    "job_title VARCHAR(35) NOT NULL" \
                    "role VARCHAR(40) NOT NULL PRIMARY KEY" \
                    ");"

    company = "CREATE TABLE Company("\
                    "company VARCHAR(100) NOT NULL PRIMARY KEY" \
                    
    
    curs.execute(location)
    curs.execute(role)
    curs.execute(company)
    
